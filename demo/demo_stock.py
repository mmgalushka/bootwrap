import numpy as np


class Share:
    """A comany share.

    Args:
        id (string): The company stock ID.
        company (string): The company name.
        logo (str): The company logo.
        description (str): The company description.
        url (str): The company URL.
        price (float): The company one share price.
    """

    def __init__(self, id, company, logo,  description, url, price):
        self.__id = id
        self.__company = company
        self.__logo = logo
        self.__description = description
        self.__url = url

        np.random.seed(0)
        mu = np.random.uniform(0.001, 0.009)
        sigma = np.random.uniform(0.01, 0.09)
        returns = np.random.normal(loc=mu, scale=sigma, size=1000)
        self.__history = price * (1 + returns).cumprod()
        self.__pointer = 0

    @property
    def id(self):
        """The ID name."""
        return self.__id

    def update(self):
        if self.__pointer >= len(self.__history):
            self.__pointer = -1
        self.__pointer += 1

    @property
    def company(self):
        """The company name."""
        return self.__company

    @property
    def logo(self):
        """The company logo."""
        return self.__logo

    @property
    def description(self):
        """The company description."""
        return self.__description

    @property
    def url(self):
        """The company one share URL."""
        return self.__url

    @property
    def price(self):
        """The company one share price."""
        return self.__history[self.__pointer]

    @price.setter
    def price(self, value):
        self.__price = value

    def __str__(self):
        return f'''
            Share(
                id: {self.id},
                company: {self.company},
                logo: {self.logo},
                description: {self.description},
                url: {self.url},
                price: {self.price}
            )
        '''


class StockMarket:
    """A stock market simulator."""

    def __init__(self):
        super().__init__()
        self.__market = {
            'GOOGL': Share(
                'GOOGL',
                'Alphabet Inc.',
                'googl-logo.png',
                'Alphabet Inc. is an American multinational conglomerate '
                'headquartered in Mountain View, California. It was created '
                'through a restructuring of Google on October 2, 2015, and '
                'became the parent company of Google and several former '
                'Google subsidiaries',
                'https://www.google.com',
                90),
            'AMZN': Share(
                'AMZN',
                'Amazon Inc.',
                'amzn-logo.png',
                'Amazon.com, Inc. is an American multinational technology '
                'company which focuses on e-commerce, cloud computing, '
                'digital streaming, and artificial intelligence. It is one '
                'of the Big Five companies in the U.S. information technology '
                'industry, along with Google, Apple, Microsoft, and Facebook.',
                'https://www.amazon.com',
                80),
            'LNKD': Share(
                'LNKD',
                'LinkedIn Inc.',
                'lnkd-logo.png',
                'LinkedIn is an American business and employment-oriented '
                'online service that operates via websites and mobile apps. '
                'Launched on May 5, 2003, the platform is mainly used for '
                'professional networking, and allows job seekers to post '
                'their CVs and employers to post jobs.',
                'https://www.linkedin.com',
                70),
            'AAPL': Share(
                'AAPL',
                'Apple Inc.',
                'aaps-logo.png',
                'Apple Inc. is an American multinational technology company '
                'that specializes in consumer electronics, computer software, '
                'and online services. Apple is the world\'s largest '
                'technology company by revenue and, since January 2021, the '
                'world\'s most valuable company.',
                'https://www.apple.com',
                75),
            'NVDA': Share(
                'NVDA',
                'NVIDIA Corporation',
                'nvda-logo.png',
                'Nvidia Corporation is an American multinational technology '
                'company incorporated in Delaware and based in Santa Clara, '
                'California. It designs graphics processing units for the '
                'gaming and professional markets, as well as system on a chip '
                'units for the mobile computing and automotive market.',
                'https://www.nvidia.com',
                125),
            'TSLA': Share(
                'TSLA',
                'Tesla, Inc.',
                'tsla-logo.png',
                'Tesla, Inc. is an American electric vehicle and clean energy '
                'company based in Palo Alto, California. Tesla\'s current '
                'products include electric cars, battery energy storage from '
                'home to grid-scale, solar panels and solar roof tiles, as '
                'well as other related products and services.',
                'https://www.tesla.com',
                125)
        }

    def update(self):
        for share in self.__market.values():
            share.update()

    def get_stocks(self):
        return self.__market.values()

    def get_stock(self, id):
        return self.__market[id]
