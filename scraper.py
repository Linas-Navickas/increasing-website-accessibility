import logging

from bs4 import BeautifulSoup


class Scraper:
    
    def file_exist(self, response, file_name):
        if response.status_code == 200:
            logging.warning(
                f"file {file_name} found. Status code: %d", response.status_code
            )
            return True
        else:
            logging.warning(
                f"file {file_name} do not found. Status code: %d", response.status_code
            )
            return False
            

    def extract_meta(self, url_soup):
        meta_description = url_soup.find("meta", attrs={"name": "description"})
        meta_keywords = url_soup.find("meta", attrs={"name": "keywords"})
        return (
            meta_description["content"] if meta_description else None,
            meta_keywords["content"] if meta_keywords else None,
        )

    def find_parent_that_doesnt_contain_h(self, tag, heading_tag):
        parent = tag.parent

        has_another_h_tag = False
        if parent is None:
            return tag

        all_parent_elements = parent.find_all()
        for element in all_parent_elements:
            if element.name.startswith("h") and element != heading_tag:
                has_another_h_tag = True

        if has_another_h_tag:
            return tag

        return self.find_parent_that_doesnt_contain_h(
            tag=parent, heading_tag=heading_tag
        )

    def extract_headings_and_content(self, html):
        soup = BeautifulSoup(markup=html, features="html.parser")

        headings = soup.find_all(["h1", "h2", "h3"])
        headings_and_content = []

        for heading in headings:
            container = self.find_parent_that_doesnt_contain_h(
                tag=heading, heading_tag=heading
            )
            elements_text = [
                el.get_text(" ", strip=True)
                for el in container
                if el.get_text(" ", strip=True) and el != heading
            ]

            heading_text = heading.get_text(" ", strip=True)
            siblings_text = " ".join(elements_text)
            if heading_text != siblings_text:
                headings_and_content.append(
                    {
                        "heading": heading_text,
                        "text": siblings_text,
                    }
                )

        text = ""
        for el in headings_and_content:
            for key, value in el.items():
                text += f"{key}: {value}\n"

        return text
