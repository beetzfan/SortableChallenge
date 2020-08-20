import json
import pandas as pd
import sys


def auction(list_of_bidders, bids_list):
    site_names = [item['name'] for item in list_of_bidders['sites']]
    site_bidders = [item['bidders'] for item in list_of_bidders['sites']][0]
    site_floor = [item['floor'] for item in list_of_bidders['sites']]
    bidder_adjustment = [item['adjustment'] for item in list_of_bidders['bidders']]
    auction_results = []
    # go through bids in input file
    count = 0
    for item in bids_list:
        auction_results.append([])
        site = item['site']
        units = item['units']
        d = {'bidder': [''] * len(units), 'bid': [0] * len(units), 'adjusted bid': [0] * len(units)}
        auction_data = pd.DataFrame(data=d, index=units)

        # check if valid website
        if site in site_names:
            index = site_names.index(site)
            # get floor value
            floor = site_floor[index]

            # check if valid bidder, unit, and bid above floor
            for bid in item['bids']:
                if bid['bidder'] in site_bidders and bid['unit'] in units and bid['bid'] > floor:
                    # adjust bids of bidders
                    index2 = site_bidders.index(bid['bidder'])
                    # check if above floor bid
                    adjustment = bidder_adjustment[index2]
                    adjust = (1 + adjustment) * bid['bid']
                    if adjust > floor:
                        # test for highest bidder
                        cur_unit = auction_data.loc[str(bid['unit'])]
                        if adjust > cur_unit['adjusted bid']:
                            auction_data.loc[str(bid['unit'])] = [bid['bidder'], bid['bid'], adjust]
            for index, row in auction_data.iterrows():
                auction_results[count].append({'bidder': row['bidder'],
                                                'bid': row['bid'],
                                                'unit': index})
            print(json.dumps(auction_results))
            count += 1
        else:
            print(json.dumps({'bidder': '',
                              'bid': '',
                              'unit': ''}))


with open('./config.json') as config:
    configuration = json.load(config)

incoming_input = json.load(sys.stdin)
auction(configuration, incoming_input)
