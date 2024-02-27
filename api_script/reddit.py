import praw
import csv

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent=''
)

subreddit_name = ''
thread_id = ''

submission = reddit.submission(id=thread_id)


submission.comments.replace_more(limit=None)
comment_list = [(comment.body, comment.score)
                for comment in submission.comments.list()]


csv_filename = 'reddit_comments.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Comment', 'Score'])
    csvwriter.writerows(comment_list)

print(f"Comments have been written to {csv_filename}")
