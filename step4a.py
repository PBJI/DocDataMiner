import glob
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def uniqueWords(txtdir=DIRNAME[1]):
    content = os.listdir(txtdir)
    dirPath = txtdir+os.sep
    content = [f'./{dirPath}{a}' for a in content]
    text_files = glob.glob(f"{txtdir}/*.txt")
    vectorizer = TfidfVectorizer(input='filename',stop_words='english')
    vectors = vectorizer.fit_transform(text_files)
    feature_names = vectorizer.get_feature_names_out()
    return feature_names
