from django.core.paginator import InvalidPage
from two.bootstrap.paginator import SectionedPaginator

from wheelcms_axle.content import type_registry
from wheelcms_axle.node import Node
from wheelcms_axle.templates import template_registry

from wheelcms_spokes.page import PageBase, PageType, PageForm
from wheelcms_spokes.file import FileType
from wheelcms_spokes.image import ImageType

from wheelcms_categories.models import CategoryType


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

class ValveBlog(PageBase):
    pass

def blog_context(handler, request, node):
    """ provide context both in Page as in Blog context """
    ## XXX This context provider will not work for non-valve (derived) blogs
    ## due to the hardcoded ValveEntry.classname dependency
    ctx = {}

    ctx['body_class'] = "wheelcms_valve"

    p = max(1, int(request.GET.get('page', 1)))
    kw = {}
    if not handler.hasaccess():
        kw['contentbase__state'] = "published"

    ## this will actually ignore the blog publication state! XXX
    ctx['paginator'] = paginator = SectionedPaginator(Node.objects.offspring(node).filter(contentbase__meta_type=ValveEntry.classname, **kw).order_by("-contentbase__created"), 4)
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
        return ValveEntry.objects.filter(
                 node__path__startswith=self.path(),
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

