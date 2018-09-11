from setuptools import setup

setup(
    name='Christopher Bot',
    version='1.0',
    description='Discord bot made with discord.py',
    url='https://github.com/skykanin/Christopher-Bot',
    author='skykanin',
    license='GNU GPLv3',
    packages=['', 'cogs/', ],
    install_requires=[
        'aiohttp',
        'dice',
        'discord.py',
        'emoji',
        'feedparser',
        'osuapi',
        'pyimgur',
        'python-twitch-client',
        'python-twitter',
        'pytz',
        'urllib3',
        'youtube-dl',
    ],
    zip_safe=False
)
