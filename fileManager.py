def write_links_to_file(links, filename):
    with open(filename, 'a') as f:
        for link in links:
            f.write(link + '\n')

def load_links_from_file(filename):
    with open(filename, 'r') as f:
        links = f.readlines()
        links = [link.strip() for link in links]
        return links

def remove_first_link_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])