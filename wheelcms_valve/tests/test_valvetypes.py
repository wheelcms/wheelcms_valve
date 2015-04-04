import pytest

from wheelcms_axle.content import TypeRegistry, type_registry
from wheelcms_axle.node import Node

from wheelcms_axle.tests.test_spoke import BaseSpokeTest, BaseSpokeTemplateTest
from wheelcms_axle.tests.test_impexp import BaseSpokeImportExportTest
from wheelcms_axle.tests.test_search import BaseTestSearch

from wheelcms_axle.tests.utils import MockedQueryDict


from ..models import ValveBlog, ValveBlogType
from ..models import ValveEntry, ValveEntryType


@pytest.mark.usefixtures("localtyperegistry")
class TestValveBlogSpokeTemplate(BaseSpokeTemplateTest):
    """ Test the ValveBlog type """
    type = ValveBlogType

    def valid_data(self, **kw):
        """ return additional data for ValveBlog validation """
        return MockedQueryDict(body="Hello World", **kw)


@pytest.mark.usefixtures("localtyperegistry")
class TestValveBlogSpoke(BaseSpokeTest):
    """ Test the ValveBlog type """
    type = ValveBlogType
    types = (ValveEntryType, )

    def test_feed(self, client, root):
        """ the feed() method is used by wheelcms_rss """
        blog = self.type.model(node=root, title="blog", state="published").save()
        spoke = blog.spoke()
        e1 = ValveEntryType.model(title="e1", state="published",
                                  node=root.add("e1")).save()
        e2 = ValveEntryType.model(title="e2", state="published",
                                  node=root.add("e2")).save()
        e3 = ValveEntryType.model(title="e3", state="private",
                                  node=root.add("e3")).save()

        assert e1 in spoke.feed()
        assert e2 in spoke.feed()
        assert e3 not in spoke.feed()

@pytest.mark.usefixtures("localtyperegistry")
class TestValveBlogSpokeImpExp(BaseSpokeImportExportTest):
    type = ValveBlogType
    spoke = ValveBlogType


@pytest.mark.usefixtures("localtyperegistry")
class TestValveBlogSpokeSearch(BaseTestSearch):
    type = ValveBlogType


@pytest.mark.usefixtures("localtyperegistry")
class TestValveEntrySpokeTemplate(BaseSpokeTemplateTest):
    """ Test the ValveEntry type """
    type = ValveEntryType

    def valid_data(self, **kw):
        """ return additional data for ValveEntry validation """
        return MockedQueryDict(body="Hello World", **kw)


@pytest.mark.usefixtures("localtyperegistry")
class TestValveEntrySpoke(BaseSpokeTest):
    """ Test the ValveEntry type """
    type = ValveEntryType


@pytest.mark.usefixtures("localtyperegistry")
class TestValveEntrySpokeImpExp(BaseSpokeImportExportTest):
    type = ValveEntryType


@pytest.mark.usefixtures("localtyperegistry")
class TestValveEntrySpokeSearch(BaseTestSearch):
    type = ValveEntryType
