def format_date(date):
  return date.strftime('%d/%b/%y')


def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

def format_plural(amount, word):
  if amount != 1:
    return word + 's'
  return word

# from datetime import datetime
# print(format_date(datetime.now()))
# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))
# print(format_url('http://google.com/test/'))
# print(format_url('https://coding-boot-camp.github.io/continuation-courses/python/lesson-3-homepage'))
# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))
# print(format_plural(0, 'road'))
# print(format_plural(10, 'computer'))
# print(format_plural(1, 'monitor'))