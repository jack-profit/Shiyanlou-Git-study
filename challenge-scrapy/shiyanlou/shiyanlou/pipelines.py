# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine, User
from scrapy.exceptions import DropItem
from datetime import datetime
from shiyanlou.items import CourseItem, UserItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)
        return item
    
    def _process_course_item(self, item):
        item['students'] = int(item['students'])
        '''
        self.session.add(Course(**item))
        return item
        '''
        if item['students'] < 2000:
            raise DropItem('Course students less than 2000.')
        else:
            self.session.add(Course(**item))

    def _process_user_item(self, item):
        item['level'] = int(item['level'][1:]) # 去掉等级前面的L
        item['join_date'] = datetime.strptime(item['join_date'], '%Y-%m-%d')
        item['learn_courses_num'] = int(item['learn_courses_num'])
        self.session.add(User(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
