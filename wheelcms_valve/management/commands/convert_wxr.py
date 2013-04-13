import pprint
from xml.dom import minidom

from xml.etree import ElementTree
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    """ 
        Import a "Wordpress eXtended RSS" file. More specifically, the one
        that zinnia currently exports. This may skip a number of relevant/
        important fields simply because zinnia doesn't support them.
    """
    args = 'readfrom [path]'
    help = 'Import an xml dump'

    def handle(self, source, *args, **kw):
        data = open(source).read()
        namespaces = {"wp": "http://wordpress.org/export/1.1/",
                      "content": "http://purl.org/rss/1.0/modules/content/",
                      "dc": "http://purl.org/dc/elements/1.1/"}
        tree = ElementTree.fromstring(data)

        # import pdb; pdb.set_trace()
        
        categories = {}

        ##
        ## categories can be nested, but are identified by a string that's
        ## not unique? Or is it. E.g.
        ## /food/bread
        ## /cooking/bread
        ##
        for cat in tree.findall("channel/wp:category", namespaces=namespaces):
            slug = cat.find("wp:category_nicename", namespaces=namespaces).text
            name = cat.find("wp:cat_name", namespaces=namespaces).text
            parent = cat.find("wp:category_parent", namespaces=namespaces).text

            categories[slug] = dict(slug=slug, name=name, items=[])

        tags = {}

        for cat in tree.findall("channel/wp:tag", namespaces=namespaces):
            slug = cat.find("wp:tag_slug", namespaces=namespaces).text
            name = cat.find("wp:tag_name", namespaces=namespaces).text

            tags[slug] = dict(slug=slug, name=name, count=0)

        items = {}
        for item in tree.findall("channel/item"):
            itemtags = []
            slug = item.find("wp:post_name", namespaces=namespaces).text

            title = item.find("title").text
            creator = item.find("dc:creator", namespaces=namespaces).text

            # print title
            for cat in item.findall("category"):
                
                domain = cat.attrib['domain']
                text = cat.text
                if domain == "category":
                    # print "\tcat:", text
                    if text not in categories:
                        #  print "Category %s not found" % text
                        pass
                    else:
                        categories[text]['items'].append(slug)

                elif domain == "tag":
                    # print "\ttag:", text
                    if text not in tags:
                        # print "Tag %s not found" % text
                        pass
                    else:
                        tags[text]['count'] += 1
                        itemtags.append(text)

            description = item.find("description", namespaces=namespaces).text
            content = item.find("content:encoded", namespaces=namespaces).text

            itemmeta = {}
            for meta in item.findall("wp:postmeta", namespaces=namespaces):
                key = meta.find("wp:meta_key", namespaces=namespaces).text
                val = meta.find("wp:meta_value", namespaces=namespaces).text
                itemmeta[key] = val

            items[slug] = dict(
                slug=slug,
                title=title,
                owner=creator,
                description=description,
                body=content,
                tags=itemtags,
                modified=itemmeta.get('_last_update', ''),
                publication=itemmeta.get('_start_publication', ''),
                expire=itemmeta.get('_end_publication', ''),
                
                state="published",
                meta_type="page", ## XXX
                navigation="False",
                template=""
            )
        #print "==categories=="
        #pprint.pprint(categories)
        #print "==tags=="
        #pprint.pprint(tags)

        ## perform the export

        root = ElementTree.Element("site")
        root.set('version', '1')
        root.set('base', '/')

        ITEM_TYPE = "wheelcms_spokes.page"
        DEFAULT_OWNER = "ivo"

        def create_field(node, name, value):
            f = ElementTree.SubElement(node, "field")
            f.attrib['name'] = name
            f.text = value
            return f

        for item in items.values():
            xmlcontent = ElementTree.SubElement(root, "content",
                         dict(slug=item['slug'],
                              type=ITEM_TYPE))
            xmlfields = ElementTree.SubElement(xmlcontent, "fields")

            for field in ("title", "description", "owner",
                          "body", "state", "meta_type", "navigation",
                          "publication", "expire", "template"):
                create_field(xmlfields, field, item.get(field, ''))

            tagsxml = ElementTree.SubElement(xmlfields, "tags")

            for tag in item['tags']:
                tagxml = ElementTree.SubElement(tagsxml, "tag")
                tagxml.text = tag

        ## flat categories, for now
        for cat in categories.values():
            if not cat['items']:
                continue

            xmlcontent = ElementTree.SubElement(root, "content",
                           dict(slug=cat['slug'],
                                type="wheelcms_categories.category"))
            xmlfields = ElementTree.SubElement(xmlcontent, "fields")
            create_field(xmlfields, "title", cat['name'])
            create_field(xmlfields, "state", "published")
            create_field(xmlfields, "owner", DEFAULT_OWNER)
            create_field(xmlfields, "navigation", "False")
            create_field(xmlfields, "meta_type", "category")

            xmlitems = ElementTree.SubElement(xmlfields, "items")
            for i in cat['items']:
                xmlitem = ElementTree.SubElement(xmlitems, "item")
                ## assume directly under root XXX
                xmlitem.text = '/' + i

            
            ## rest is defaults

            ## state, navigation, template
            ## map owner
            ## tags

        print minidom.parseString(ElementTree.tostring(root, "utf-8")).toprettyxml(indent="  ").encode("utf-8")
        ## export categories
        ## -- items

