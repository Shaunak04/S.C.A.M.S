# temp = [
#     {
#         'weight': 50,
#         'dimension': {
#             'width': 30,
#             'height': 30,
#             'breadth': 30
#         },
#         'container_no': 0
#     },
#     {
#         'weight': 23,
#         'dimension': {
#             'width': 30,
#             'height': 40,
#             'breadth': 50
#         },
#         'container_no': 0
#     },
#     {
#         'weight': 16,
#         'dimension': {
#             'width': 50,
#             'height': 40,
#             'breadth': 50
#         },
#         'container_no': 0
#     },
#     {
#         'weight': 18,
#         'dimension': {
#             'width': 60,
#             'height': 70,
#             'breadth': 20
#         },
#         'container_no': 0
#     },
#     {
#         'weight': 24,
#         'dimension': {
#             'width': 20,
#             'height': 20,
#             'breadth': 20
#         },
#         'container_no': 0
#     },
# ]

# calculates volume of a bag
def bag_vol(bag):
    return (float(bag['dimension']['width']) * float(bag['dimension']['breadth']) * float(bag['dimension']['height']))

# calculates weight by volume ration, which is the metric for 0/1 knapsack
def value(bag):
    return float(bag['weight']) / bag_vol(bag)


def knapsack(luggage: list):
    containers =    {
        1: {'list': [], 'weight': 0, 'volume': 0},
        2: {'list': [], 'weight': 0, 'volume': 0},
        3: {'list': [], 'weight': 0, 'volume': 0},
        4: {'list': [], 'weight': 0, 'volume': 0},
        5: {'list': [], 'weight': 0, 'volume': 0},
        6: {'list': [], 'weight': 0, 'volume': 0},
        7: {'list': [], 'weight': 0, 'volume': 0},
    }

    wt_container = 3402.0
    vol_container = 402402.0

    luggage.sort(key=value) # sort with custom comparator

    # initialization
    container_id = 1
    bag_id = 0

    while bag_id != len(luggage):
        bag = luggage[bag_id]
        if float(containers[container_id]['weight']) + float(bag['weight']) <= wt_container and float(containers[container_id]['volume']) + bag_vol(bag) <= vol_container:
            containers[container_id]['list'].append(bag)
            containers[container_id]['weight'] += float(bag['weight'])
            containers[container_id]['volume'] += bag_vol(bag)
            print('Added to container')
            luggage[bag_id]['container_no'] = container_id
            bag_id += 1
            print('Next Bag')
            
        else:
            print('Not Added to container')
            container_id += 1
            if container_id > 7:
                print('Storage Limit Exceeded')
    print(containers)
    return luggage