# -*- coding: utf-8 -*-
import scrapy
from ..items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['shiyanlou.com']

    @property
    def start_urls(self):
        url = 'https://www.shiyanlou.com/courses/'
        url_list = [url, url+'?page=2', url+'?page=3']
        return url_list

    def parse(self, response):
        for course in response.css('div.col-md-3'):
            item = CourseItem({
                'name': course.css('h6::text').extract_first().strip(),
                'description': course.css('div.course-description::text').extract_first().strip(),
                'type': course.css('span.course-type::text').extract_first().strip(),
                'students': course.css('span.students-count span::text').extract_first().strip()
                })
            yield item

