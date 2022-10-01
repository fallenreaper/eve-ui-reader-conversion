from base import *
import json

base1='sample.json'
base2withimage='eve-online-memory-reading-8ae367ddee.json'
with open(base2withimage) as fp:
  data = json.load(fp)

print("Entries: ", len(data))

u: UITreeNode = UITreeNode.fromJson(data)
print(u.dictEntriesOfInterest, u.pythonObjectAddress, u.pythonObjectTypeName)


ui = parseUserinterfaceFromUITree(parseUITreeWithDisplayRegionFromUITree(u))
print("Chat Window Stacks", ui.chatWindowStacks)

if ui.chatWindowStacks is not None:
  print("Dumping Chat windows and Usernames")
  for cWindow in ui.chatWindowStacks:
    print("Window Name: ", cWindow.chatWindow.name)
    print("Users", [(x.name, x.standingIconHint) for x in cWindow.chatWindow.userlist.visibleUsers])

if ui.dronesWindow is not None:
  print("Drone Window")
  print(ui.dronesWindow)
  print(f"Drones in Bay: ${len(ui.dronesWindow.droneGroupInBay.children)}")
  print(f"Drones in Space: ${len(ui.dronesWindow.droneGroupInLocalSpace.children)}")

if ui.overviewWindow is not None:
  print("Overview Window")
  print(ui.overviewWindow)
  print("Items In Overview: ")
  print([ x.objectName for x in ui.overviewWindow.entries if x.objectName is not None])


print("Target Information")
[(x.textsTopToBottom, x.isActiveTarget) for x in ui.targets]