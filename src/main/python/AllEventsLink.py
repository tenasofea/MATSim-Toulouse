import xml.etree.ElementTree as ET

def list_events_same_link(xml_file, link_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    events_same_link = []
    for event in root.findall('event'):
        if event.get('link') == link_id:
            person_id = event.get('person')
            vehicle_id = event.get('vehicle')
            time = event.get('time')
            facility = event.get('facility')
            act_type = event.get('actType')
            
            events_same_link.append({
                'person': person_id,
                'vehicle': vehicle_id,
                'time': time,
                'facility': facility,
                'link': link_id,
                'actType': act_type
            })
    
    return events_same_link

xml_file = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_5000.xml"
link_id = '106590'

events = list_events_same_link(xml_file, link_id)

for event in events:
    print(f"Personne: {event['person']}, Vehicle: {event['vehicle']}, Temps: {event['time']}, Facility: {event['facility']}, Lien: {event['link']}, Type d'activite: {event['actType']}")
