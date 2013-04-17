from django.core.paginator import Paginator, InvalidPage

from wheelcms_axle.content import type_registry
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

    class form(PageForm):
        """ derive from Page's form but with correct model """
        class Meta(PageForm.Meta):
            model = ValveEntry

    icon = "blogs.png"

class ValveBlog(PageBase):
    pass

class SectionedPaginator(Paginator):
    def sections(self, page, windowsize=6):
        np = self.num_pages

        b = m = e = []

        ##
        ## provide sort of a sliding window over the available
        ## pages with the current page in the center.
        ## windowsize is the size of this window
        if np > windowsize*2:
            b = [1]
            e = [np]
            start = max(3, page - windowsize/2)
            end = start + windowsize+1
            if end > np-2:
                end = np - 1
                start = end - windowsize - 1

            if page < 4:
                b = range(1, windowsize)
                e = [np]
            elif page > (np - 3):
                b = [1]
                e = range(np+1-windowsize, np+1)
            else:
                m = range(start, end)
        else:
            b = range(1, np + 1)

        return b, m, e

class ValveBlogType(PageType):
    model = ValveBlog
    title = "A Valve blog"
    children = (FileType, ImageType, ValveEntryType, CategoryType)

    class form(PageForm):
        """ derive from Page's form but with correct model """
        class Meta(PageForm.Meta):
            model = ValveBlog

    icon = "blogs.png"

    def context(self, handler, request, node):
        ctx = super(ValveBlogType, self).context(handler, request, node)


        p = max(1, int(request.GET.get('page', 1)))
        ctx['paginator'] = paginator = SectionedPaginator(self.instance.node.childrenq(contentbase__meta_type=ValveEntry.classname).order_by("-contentbase__created"), 4)
        b, m, e = paginator.sections(p, windowsize=6)
        ctx['begin'] = b
        ctx['middle'] = m
        ctx['end'] = e

        try:
            ctx['page'] = paginator.page(p)
        except InvalidPage:
            ctx['page'] = paginator.page(1)

        return ctx

type_registry.register(ValveBlogType)
template_registry.register(ValveBlogType, "wheelcms_valve/valveblog_view.html",
                           "Blog view", default=True)
type_registry.register(ValveEntryType)
template_registry.register(ValveEntryType, "wheelcms_valve/valveentry_view.html",
                           "Blog entry view", default=True)
