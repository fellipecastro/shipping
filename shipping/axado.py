#!/usr/bin/env python
# coding: utf-8

import sys
import re
import csv
from decimal import Decimal

from settings import DATABASES


class Axado():

    def __init__(self, argv):
        if Axado.check_arguments(argv):
            self.origin = argv[1].lower()
            self.destination = argv[2].lower()
            self.receipt = float(argv[3])
            self.weight = float(argv[4])
            # self.receipt = float(Decimal(argv[3]).quantize(
            #     Decimal('.01'), rounding='ROUND_UP'))
            # self.weight = float(Decimal(argv[4]).quantize(
            #     Decimal('.01'), rounding='ROUND_UP'))

            # print "%s - %s - %s - %s" % (
            #     self.origin, self.destination, self.receipt, self.weight)

            self.table()
            self.table2()

    @staticmethod
    def is_valid_city_name(city_name):
        return re.match("^[a-zA-Z]+$", city_name) is not None

    @staticmethod
    def is_valid_number(number):
        return re.match("^\d+\.?\d*$", number) is not None

    @staticmethod
    def check_arguments_length(argv):
        return True if len(argv) == 5 else False

    @staticmethod
    def check_arguments_type(argv):
        return True if Axado.is_valid_city_name(argv[1])\
            and Axado.is_valid_city_name(argv[2])\
            and Axado.is_valid_number(argv[3])\
            and Axado.is_valid_number(argv[4]) else False

    def lookup_table_routes(self):
        with open(DATABASES['table']['routes']) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['origem'] == self.origin and row['destino'] ==
                        self.destination):
                    self.delivery_time = int(row['prazo'])
                    self.insurance = float(row['seguro'])
                    self.kg = row['kg']
                    self.fixed = float(row['fixa'])
                    return True
        return False

    def lookup_table_price_per_kg(self):
        with open(DATABASES['table']['price_per_kg']) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['nome'] == self.kg and (
                        float(row['inicial']) <= self.weight <=
                        float(row['final']))):
                    self.price_per_kg = float(row['preco'])
                    return True
        return False

    @staticmethod
    def check_arguments(argv):
        if not Axado.check_arguments_length(argv):
            print """It is required 4 arguments in order to successfuly \
calculate shipping.\n
They are: <origin> <destination> <receipt> <weight>.\n
e.g., florianopolis brasilia 50 7"""
        elif not Axado.check_arguments_type(argv):
            print """Whereas the first two arguments should be valid city \
names, third and fourth ones should be valid numbers.\n
e.g., florianopolis brasilia 50 7"""
        else:
            return True
        return False

    def sum_insurance(self):
        self.subtotal = self.receipt * self.insurance / 100

    def sum_fixed(self):
        self.subtotal += self.fixed

    def sum_weight_price(self):
        self.subtotal += self.price_per_kg * self.weight

    def sum_icms(self):
        self.subtotal += self.subtotal / ((100 - self.icms) / 100)

    def table(self):
            self.delivery_time = "-"
            self.price = "-"
            self.icms = 6.0

            if self.lookup_table_routes():
                if self.lookup_table_price_per_kg():
                    self.price = self.price_per_kg

            self.sum_insurance()
            print "SUBTOTAL: %s" % self.subtotal
            self.sum_fixed()
            print "SUBTOTAL: %s" % self.subtotal
            self.sum_weight_price()
            print "SUBTOTAL: %s" % self.subtotal
            self.sum_icms()
            print "SUBTOTAL: %s" % self.subtotal
            self.price = float(Decimal(self.subtotal).quantize(
                Decimal('.01'), rounding='ROUND_UP'))
            print "tabela:%s, %s" % (self.delivery_time, self.price)

    def table2(self):
        self.delivery_time = "-"
        self.price = "-"
        print "tabela2:%s, %s" % (self.delivery_time, self.price)

if __name__ == '__main__':
    axado = Axado(sys.argv)
