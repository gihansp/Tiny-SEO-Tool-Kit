import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def seo_check():
    url = url_entry.get()
    keywords = keywords_entry.get().split(',')
    result = ''

    # URL length check
    if len(url) <= 60:
        result += 'URL length is less than 60 characters\n'
    else:
        result += 'URL length is more than 60 characters\n'

    # Keywords in URL check
    for keyword in keywords:
        if keyword in url:
            result += f'Keyword "{keyword}" is present in URL\n'
        else:
            result += f'Keyword "{keyword}" is not present in URL\n'

    # Start web driver
    options = Options()
    options.add_argument('-headless')

    # Start web driver
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Keywords on page check
    for keyword in keywords:
        keyword_count = len(driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]"))
        result += f'Keyword "{keyword}" is present {keyword_count} times on page\n'

    # SEO stopwords check
    stopwords = ['a', 'an', 'and', 'the', 'of', 'in', 'to', 'with', 'for', 'by', 'on']
    for stopword in stopwords:
        if stopword in url:
            result += f'SEO stopword "{stopword}" is present in URL\n'

    # URL syntax check
    if '_' in url:
        result += 'URL uses underscores for word separations\n'
    else:
        result += 'URL uses hyphens for word separations\n'

    # Title tag check
    title_tag = driver.find_element(By.XPATH, '//head/title').get_attribute('innerHTML')
    title_keywords = [keyword for keyword in keywords if keyword in title_tag]
    if title_keywords:
        result += f'Title tag includes keywords: {title_keywords}\n'
    else:
        result += 'Title tag does not include any of the keywords\n'

    # Meta description check
    meta_description = driver.find_element(By.XPATH, '//head/meta[@name="description"]').get_attribute('content')
    description_keywords = [keyword for keyword in keywords if keyword in meta_description]
    if description_keywords:
        result += f'Meta description includes keywords: {description_keywords}\n'
    else:
        result += 'Meta description does not include any of the keywords\n'

    # Image check
    images = driver.find_elements(By.XPATH, '//img')
    for image in images:
        alt_text = image.get_attribute('alt')
        file_name = image.get_attribute('src').split('/')[-1]
        if not alt_text:
            result += 'Image is missing alt text\n'
        if '_' in file_name or not file_name.strip():
            result += 'Image file name is not search engine friendly\n'
        else:
            result += 'Image file name is search engine friendly\n'

    # Show result
    result_label.config(text=result)

    # Close web driver
    driver.quit()


# Tkinter GUI
root = tk.Tk()
root.title("SEO Checker")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

keywords_label = tk.Label(root, text="Enter keywords separated by comma:")
keywords_label.pack()

keywords_entry = tk.Entry(root)
keywords_entry.pack()

check_button = tk.Button(root, text="Check", command=seo_check)
check_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
