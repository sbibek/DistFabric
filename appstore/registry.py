from appstore.testapp.testapp import TestApp
from appstore.search.search import DfSearchApp

apps = {
    'search': { 'description': 'search in directory on words from wordslist (usage: invoke search $dirpath $wordlistpath)', 'instance': DfSearchApp() }
}