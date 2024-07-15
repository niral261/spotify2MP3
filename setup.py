from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pandas',
    'gunicorn',
    'python-dotenv'
]


setup(
    name='spotify2MP3',
    version='1.0.0',
    description='An app to get youtube MP3 file from your spotify songs',
    author='Niral Ajmera',
    author_email='ajmeraniral@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)