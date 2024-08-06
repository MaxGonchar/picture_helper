import csv

import dao
from utils import hash_tag

tags = [hash_tag(tag) for tag in dao.get_all_tags()] + ["is_good"]

if len(tags) != len(set(tags)):
    raise Exception("Duplicate headers found")

with open('images.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(tags)

    for img in dao.get_images():
        img_tags = [hash_tag(tag) for tag in img.tags]
        row = [int(tag in img_tags) for tag in tags[:-1]] + [int(img.is_good)]
        writer.writerow(row)
