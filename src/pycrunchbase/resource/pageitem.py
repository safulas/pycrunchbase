import six


class PageItem(object):
    """A item within a Page.

    A page is a homogenous collection of PageItem, and there are many
    kinds of PageItem. :meth:`build` is a helper class method to
    help build the correct type of PageItem based on

    1. path, or
    2. type
    """
    def __init__(self, data):
        self.data = data
        for k, v in six.iteritems(data):
            setattr(self, k, v)
        if 'path' in self.data:
            setattr(self, 'cb_url', 'crunchbase.com/' + data.get('path'))

    @classmethod
    def build(cls, data):
        path = data.get('type', '')
        if path == 'Acquisition':
            from .acquisition import AcquisitionRelationship
            return AcquisitionRelationship(data)
        if path == 'FundingRound':
            from .fundinground import FundingRound
            return FundingRound(data)
        if path == 'Ipo':
            from .ipo import IPO
            return IPO(data)
        if path == 'Organization':
            from .organization import Organization
            return Organization(data)
        if path == 'Person':
            from .person import Person
            return Person(data)
        if path.startswith('product'):
            from .product import Product
            return Product(data)
        if data.get('type') == 'InvestorInvestment':
            return InvestorInvestmentPageItem(data)
        if path.startswith('location'):
            return LocationPageItem(data)
        if path.startswith('category'):
            return CategoryPageItem(data)
        if path == 'Fund':
            from .fund import Fund
            return Fund(data)
        if path == 'Job':
            from .job import Job
            return Job(data)
        if path == 'Address':
            from .address import Address
            return Address(data)
        return cls(data)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'PageItem: %s' % self.data


class UuidPageItem(PageItem):
    def __init__(self, data):
        uuid = data.get('uuid')
        setattr(self, 'uuid', uuid)
        super(UuidPageItem, self).__init__(data)


class PermalinkPageItem(PageItem):
    def __init__(self, data):
        permalink = data.get('properties', {}).get('permalink')
        setattr(self, 'permalink', permalink)
        super(PermalinkPageItem, self).__init__(data)


@six.python_2_unicode_compatible
class AcquisitionPageItem(UuidPageItem):
    def __str__(self):
        return u'{name} {announced_on}'.format(
            name=self.name,
            announced_on=self.announced_on,
        )


@six.python_2_unicode_compatible
class FundingRoundPageItem(UuidPageItem):
    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class InvestorInvestmentPageItem(PageItem):
    def __init__(self, data):
        super(InvestorInvestmentPageItem, self).__init__(data)
        if 'investor' in data:
            self.investor = PageItem.build(self.investor)
        if 'invested_in' in data:
            self.invested_in = PageItem.build(self.invested_in)

    def __str__(self):
        return u'{investor} ${money}'.format(
            investor=self.investor,
            money=self.money_invested_usd,
        )


@six.python_2_unicode_compatible
class LocationPageItem(UuidPageItem):
    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class CategoryPageItem(UuidPageItem):
    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class NonePageItem(PageItem):
    def __init__(self):
        super(NonePageItem, self).__init__({})

    def __getattr__(self, attr):
        return None

    def __len__(self):
        return 0

    def __str__(self):
        return 'NonePageItem'

NonePageItemSingleton = NonePageItem()
