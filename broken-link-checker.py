import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class BrokenLinkChecker:
    def __init__(self, master):
        self.master = master
        self.master.title("Broken Link Checker")
        self.master.geometry("300x150")

        self.url_label = tk.Label(self.master, text="Enter URL:")
        self.url_entry = tk.Entry(self.master, width=30)
        self.check_button = tk.Button(self.master, text="Check", command=self.check_links)

        self.url_label.pack()
        self.url_entry.pack()
        self.check_button.pack()

    def check_links(self):
        url = self.url_entry.get()
        broken_links = []

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")
            progress_bar = tqdm(total=len(links), desc="Checking links...")

            for link in links:
                href = link.get("href")
                try:
                    response = requests.get(href)
                    if response.status_code != 200:
                        broken_links.append(href)
                except Exception:
                    broken_links.append(href)

                progress_bar.update(1)

            if broken_links:
                messagebox.showerror("Broken Links", "\n".join(broken_links))
            else:
                messagebox.showinfo("Broken Links", "No broken links found.")

            progress_bar.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = BrokenLinkChecker(root)
    root.mainloop()


