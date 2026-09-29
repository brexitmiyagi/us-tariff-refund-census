# Who carried the IEEPA duties, against who gets them back.
# Two published estimates, combined. The consumer share is a floor, so the business share is a ceiling.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import inputs

x = inputs()
total = x["ieepa_duties_total"]
foreign = total * x["foreign_share_of_burden"]
consumers = total * x["consumer_passthrough_floor"]
business = total - foreign - consumers
print("IEEPA duties: %.0fbn" % total)
print("Foreign exporters (about 10%%): %.1fbn" % foreign)
print("US consumers (at least 30%%): %.1fbn" % consumers)
print("US businesses (residual, a ceiling): %.1fbn" % business)
print("Refund paid to importers of record: %.0fbn plus interest" % total)
print("Refund that repays cost carried by someone other than the importer, at least: %.1fbn" % (foreign + consumers))
