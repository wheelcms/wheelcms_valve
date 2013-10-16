from django.core.paginator import InvalidPage
from two.bootstrap.paginator import SectionedPaginator

from wheelcms_axle.content import type_registry
from wheelcms_axle.node import Node, node_proxy_factory
from wheelcms_axle.templates import template_registry
from wheelcms_axle.utils import get_active_language

from wheelcms_spokes.page import PageBase, PageType, PageForm
from wheelcms_spokes.file import FileType
from wheelcms_spokes.image import ImageType

from wheelcms_categories.models import Category, CategoryType


class ValveEntry(PageBase):
    pass

class ValveEntryType(PageType):
    model = ValveEntry
    title = "A Valve entry"
    implicit_add = False

    discussable = True  ## entries can be discussed, of course

    children = (FileType, ImageType)

    class form(PageForm):
        """ derive from Page's form but with correct model """
        class Meta(PageForm.Meta):
            model = ValveEntry

    icon = "blogs.png"

    def context(self, handler, request, node):
        ctx = super(ValveEntryType, self).context(handler, request, node)

        ## Category.objects.parent(my_parent) ?
        language = handler.active_language()
        parent = handler.instance.parent()
        ctx['blog'] = parent.content(language=language)
        ctx['categories'] = Category.objects.filter(
                            node__tree_path__startswith=parent.tree_path + '/',
                            language=language).order_by("node__position")
        return ctx

class ValveBlog(PageBase):
    pass

def blog_context(handler, request, node):
    """ provide context both in Page as in Blog context """
    ## XXX This context provider will not work for non-valve (derived) blogs
    ## due to the hardcoded ValveEntry.classname dependency
    ctx = {}

    ctx['body_class'] = "wheelcms_valve"

    try:
        p = max(1, int(request.GET.get('page', 1)))
    except (ValueError, TypeError):
        p = 1

    kw = {}
    if not handler.hasaccess():
        kw['contentbase__state'] = "published"

    language = get_active_language(request)
    kw['contentbase__language'] = language

    category_slug = request.GET.get('category', '')
    if category_slug:
        ## XXX Untested
        category = handler.instance.child(category_slug, language=language)
        kw['contentbase__categories'] = category

    try:
        ownerid = int(request.GET.get('ownerid', ''))
        kw['contentbase__owner__id'] = ownerid
    except ValueError:
        pass
    ## this will actually ignore the blog publication state! XXX
    ctx['paginator'] = paginator = SectionedPaginator(
         node_proxy_factory(Node, language)
         .objects.offspring(node)
         .filter(contentbase__meta_type=ValveEntry.classname, **kw)
         .order_by("-contentbase__created"), 4)
    b, m, e = paginator.sections(p, windowsize=6)
    ctx['begin'] = b
    ctx['middle'] = m
    ctx['end'] = e

    try:
        ctx['page'] = paginator.page(p)
    except InvalidPage:
        ctx['page'] = paginator.page(1)

    return ctx

class ValveBlogType(PageType):
    model = ValveBlog
    title = "A Valve blog"
    children = (FileType, ImageType, ValveEntryType, CategoryType)
    primary = ValveEntryType

    class form(PageForm):
        """ derive from Page's form but with correct model """
        class Meta(PageForm.Meta):
            model = ValveBlog

    icon = "blogs.png"

    def context(self, handler, request, node):
        ctx = super(ValveBlogType, self).context(handler, request, node)
        ctx.update(blog_context(handler, request, node))

        return ctx

    def feed(self):
        ## XXX Use content object manager once available
        return ValveEntry.objects.filter(
                 node__tree_path__startswith=self.instance.node.tree_path,
                 state="published").order_by("-created")

def global_blog_context(handler, request, node):
    ctx = blog_context(handler, request, node)
    ctx['all_blogs'] = ValveBlog.objects.filter(state="published")
    ctx['global_context'] = True

    return ctx

type_registry.register(ValveBlogType)
template_registry.register(ValveBlogType, "wheelcms_valve/valveblog_view.html",
                           "Blog view", default=True)
type_registry.register(ValveEntryType)
template_registry.register(ValveEntryType, "wheelcms_valve/valveentry_view.html",
                           "Blog entry view", default=True)

template_registry.register(PageType, "wheelcms_valve/valveblog_view.html",
                           "Blog view", default=False,
                           context=global_blog_context)

