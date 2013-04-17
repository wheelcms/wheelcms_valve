from wheelcms_axle.content import TypeRegistry, type_registry
from wheelcms_axle.tests.test_spoke import BaseSpokeTest, BaseSpokeTemplateTest
from wheelcms_axle.tests.test_impexp import BaseSpokeImportExportTest
from wheelcms_axle.tests.test_search import BaseTestSearch


from ..models import ValveBlog, ValveBlogType
from ..models import ValveEntry, ValveEntryType


class TestValveBlogSpokeTemplate(BaseSpokeTemplateTest):
    """ Test the ValveBlog type """
    type = ValveBlogType

    def valid_data(self):
        """ return additional data for ValveBlog validation """
        return dict(body="Hello World")


class TestValveBlogSpoke(BaseSpokeTest):
    """ Test the ValveBlog type """
    type = ValveBlogType


class TestValveBlogSpokeImpExp(BaseSpokeImportExportTest):
    type = ValveBlog
    spoke = ValveBlogType


class TestValveBlogSpokeSearch(BaseTestSearch):
    type = ValveBlogType


class TestValveEntrySpokeTemplate(BaseSpokeTemplateTest):
    """ Test the ValveEntry type """
    type = ValveEntryType

    def valid_data(self):
        """ return additional data for ValveEntry validation """
        return dict(body="Hello World")


class TestValveEntrySpoke(BaseSpokeTest):
    """ Test the ValveEntry type """
    type = ValveEntryType


class TestValveEntrySpokeImpExp(BaseSpokeImportExportTest):
    type = ValveEntry
    spoke = ValveEntryType


class TestValveEntrySpokeSearch(BaseTestSearch):
    type = ValveEntryType
