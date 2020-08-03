import arxiv
import datetime
import pytz
from googletrans import Translator
translator = Translator()
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def collect_arxiv():
    dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    dt_old = dt_now - datetime.timedelta(days=7)
    dt_now = dt_now.strftime('%Y%m%d')
    dt_day = dt_old.strftime('%Y%m%d')
    dt_last = dt_now + '115959'
    cv_papers = arxiv.query(query='cat:cs.cv AND submittedDate:[{} TO {}]'.format(dt_day, dt_now), sort_by='submittedDate')
    if len(cv_papers) > 100:
        cv_papers = cv_papers[:100]
    
    cv_all_dict = {}
    for i, cv_paper in enumerate(cv_papers):
        number = str(i+1)
        id = cv_paper['id']
        title = cv_paper['title']
        pdf = cv_paper['pdf_url']
        summary = cv_paper['summary']
        summary = ''.join(summary.splitlines())
        summary_ja = translator.translate(summary, src='en', dest='ja')
        summary_ja = str(summary_ja.text)
        cv_dict = {"id": id, "title": title, "pdf": pdf, "summary": summary, "summary_ja": summary_ja}
        cv_all_dict[number] = cv_dict

    return cv_all_dict


def main():
    paper_list = collect_arxiv()
    cred = credentials.Certificate('')
    firebase_admin.initialize_app(cred, {
        'databaseURL': '',
        'databaseAuthVariableOverride': {
            'uid': 'my-service-worker'
        }
    })
    ##databaseに初期データを追加する
    users_ref = db.reference('/papers')
    users_ref.set(paper_list)
    print(users_ref.get())



if __name__ == '__main__':
    main()
