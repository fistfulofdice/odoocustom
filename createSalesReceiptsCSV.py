#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Copyright 2015 InfoCentrality Ltd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__revision__ = ""                                                               
__version__ = "1.1"                                                             
__author__ = "Trevor Hennion, trevor@infocentrality.co.uk"

#############
debug = True
debug = False
#############

inputFileName="04-2015.csv"
nameSplit = inputFileName.split("-")

period = nameSplit[0]+"/"+nameSplit[1]
if debug: print period

outputFileName="salesJournalFigures-"+nameSplit[0]+"-"+nameSplit[1]+".csv"
if debug: print outputFileName
periodID = '"%s"' % period
line1Format = {'date':'',
              'period':'',
              'journal':'"SAJ"',
              'name':'',
              'line_id/account':'"Sales category 1"',
              'line_id/date':'',
              'line_id/name':'"old sales"',
               'line_id/journal':'"SAJ"',
               'line_id/credit':'',
               'line_id/debit':'',
               'line_id/tax_code_id':'"Total value of sales ex VAT (box 8 included)"',
               'line_id/tax_amount':''}
line2Format = {'date':'',
              'period':'',
              'journal':'',
              'name':'',
              'line_id/account':'"Sales Tax Control Account"',
              'line_id/date':'',
              'line_id/name':'"old sales"',
               'line_id/journal':'"SAJ"',
               'line_id/credit':'',
               'line_id/debit':'',
               'line_id/tax_code_id':'"VAT on Sales and other outputs"',
               'line_id/tax_amount':''}
line3Format = {'date':'',
              'period':'',
              'journal':'',
              'name':'',
              'line_id/account':'"Bank"',
              'line_id/date':'',
              'line_id/name':'"old sales"',
               'line_id/journal':'"SAJ"',
               'line_id/credit':'',
               'line_id/debit':'',
               'line_id/tax_code_id':'',
               'line_id/tax_amount':''}
lineOutputFormat = ['date',
                   'period',
                   'journal',
                   'name',
                   'line_id/account',
                   'line_id/date',
                   'line_id/name',
                   'line_id/journal',
                   'line_id/credit',
                   'line_id/debit',
                   'line_id/tax_code_id',
                   'line_id/tax_amount']

topLine = '"'+'","'.join(lineOutputFormat)+'"\n'
if debug: print topLine
of = open(outputFileName,'w')
# Write top line of output file
of.write(topLine)

inf = open(inputFileName,'r')
infLines = inf.readlines()
inf.close()
infLineFormat = ['date','exVAT','VAT','Total']

if debug: print "Length Input file",len(infLines)

for index,line in enumerate(infLines):
    lineData = []
    line1Output = []
    line2Output = []
    line3Output = []
    if index==0:
        # Skip description line
        continue
    if debug and index==2:
        # Break for testing
        break
    if debug: print line
    lineItems = line.split(',')
    if debug: print lineItems
    # First line
    for key in lineOutputFormat:
        if key=="date":
            # Change date to ISO format
            date = lineItems[infLineFormat.index('date')]
            dateString = date.split("/")
            newDate = dateString[2]+"-"+dateString[1]+"-"+dateString[0]
            line1Output.append('"%s"' % newDate)
        elif key=="period":
            line1Output.append(periodID)
        elif key=="name":
            line1Output.append('"%s"' % newDate)
        elif key=="line_id/date":
            line1Output.append('"%s"' % newDate)
        elif key=="line_id/credit":
            line1Output.append(lineItems[infLineFormat.index('exVAT')])
        elif key=="line_id/debit":
            line1Output.append('0')
        elif key=="line_id/tax_amount":
            line1Output.append(lineItems[infLineFormat.index("exVAT")])
        else:
            line1Output.append(line1Format[key])
    # Write first line to output file
    lineData = ','.join(line1Output)+"\n"
    if debug: print lineData
    of.write(lineData)
    # Second line
    for key in lineOutputFormat:
        if key=="line_id/date":
            line2Output.append('"%s"' % newDate)
        elif key=="line_id/credit":
            line2Output.append(lineItems[infLineFormat.index('VAT')])
        elif key=="line_id/debit":
            line2Output.append('0')
        elif key=="line_id/tax_amount":
            line2Output.append(lineItems[infLineFormat.index('VAT')])
        else:
            line2Output.append(line2Format[key])
    lineData = ','.join(line2Output)+"\n"
    if debug: print lineData
    of.write(lineData)
    # Third line
    for key in lineOutputFormat:
        if key=="line_id/date":
            line3Output.append('"%s"' % newDate)
        elif key=="line_id/credit":
            line3Output.append('0')
        elif key=="line_id/debit":
            line3Output.append(lineItems[infLineFormat.index('Total')].strip())
        else:
            line3Output.append(line3Format[key])
    lineData = ','.join(line3Output)+"\n"
    if debug: print lineData
    of.write(lineData)
# Close output file
of.close()
if debug: print "Loops",index
