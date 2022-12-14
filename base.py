# module EveOnline.ParseUserinterface exposing (..)
# -| A library of building blocks to build programs that read from the EVE Online game client.
# The EVE Online client's UI tree can contain thousands of nodes and tens of thousands of individual properties. Because of this large amount of datanavigating in there can be time-consuming.
# This library helps us navigate the UI tree with functions to filter out redundant data and extract the interesting bits.
# The types in this module provide names more closely related to players' experiencesuch as the overview window or ship modules.
# To learn about the user interface structures in the EVE Online game clientsee the guide at <https://to.botlab.org/guide/parsed-user-interface-of-the-eve-online-game-client>
# -
# import Common.EffectOnWindow
# import Dict
# import EveOnline.MemoryReading
# import Json.Decode
# import List.Extra
# import Maybe.Extra
# import Regex
# import Set

from math import pi
from classes import *
from typing import Callable, Tuple
from helpers import *
from copy import copy

from pprint import pprint


def parseUITreeWithDisplayRegionFromUITree(uiTree: UITreeNode) -> UITreeNodeWithDisplayRegion:
    selfDisplayRegion = getDisplayRegionFromDictEntries(
        uiTree) or DisplayRegion(**{'x': 0, 'y': 0, 'width': 0, 'height': 0})
    return asUITreeNodeWithDisplayRegion(selfDisplayRegion, selfDisplayRegion, uiTree)
# parseUITreeWithDisplayRegionFromUITree : UITreeNode -> UITreeNodeWithDisplayRegion
# parseUITreeWithDisplayRegionFromUITree uiTree =
#     let
#         selfDisplayRegion =
#             uiTree |> getDisplayRegionFromDictEntries |> Maybe.withDefault { x = 0, y = 0, width = 0, height = 0 }
#     in
#     uiTree
#         |> asUITreeNodeWithDisplayRegion
#             { selfDisplayRegion = selfDisplayRegion
#             , totalDisplayRegion = selfDisplayRegion
#             }


def parseUserinterfaceFromUITree(uiTree: UITreeNodeWithDisplayRegion) -> ParsedUserInterface:
    x = ParsedUserInterface()
    x.uiTree = uiTree
    x.contextMenus = parseContextMenusFromUITreeRoot(uiTree)
    x.shipUI = parseShipUIFromUITreeRoot(uiTree)
    x.targets = parseTargetsFromUITreeRoot(uiTree)
    # x.infoPanelContainer = parseInfoPanelContainerFromUIRoot(uiTree)
    x.overviewWindow = parseOverviewWindowFromUITreeRoot(uiTree)
    x.selectedItemWindow = parseSelectedItemWindowFromUITreeRoot(uiTree)
    x.dronesWindow = parseDronesWindowFromUITreeRoot(uiTree)
    # x.fittingWindow = parseFittingWindowFromUITreeRoot(uiTree)
    x.probeScannerWindow = parseProbeScannerWindowFromUITreeRoot(uiTree)
    x.directionalScannerWindow = parseDirectionalScannerWindowFromUITreeRoot(
        uiTree)
    x.stationWindow = parseStationWindowFromUITreeRoot(uiTree)
    # x.inventoryWindows = parseInventoryWindowsFromUITreeRoot(uiTree)
    x.moduleButtonTooltip = parseModuleButtonTooltipFromUITreeRoot(uiTree)
    x.chatWindowStacks = parseChatWindowStacksFromUITreeRoot(uiTree)
    # x.agentConversationWindows = parseAgentConversationWindowsFromUITreeRoot(
    #     uiTree)
    # x.marketOrdersWindow = parseMarketOrdersWindowFromUITreeRoot(uiTree)
    # x.surveyScanWindow = parseSurveyScanWindowFromUITreeRoot(uiTree)
    x.bookmarkLocationWindow = parseBookmarkLocationWindowFromUITreeRoot(
        uiTree)
    # x.repairShopWindow = parseRepairShopWindowFromUITreeRoot(uiTree)
    # x.characterSheetWindow = parseCharacterSheetWindowFromUITreeRoot(uiTree)
    # x.fleetWindow = parseFleetWindowFromUITreeRoot(uiTree)
    # x.watchListPanel = parseWatchListPanelFromUITreeRoot(uiTree)
    # x.standaloneBookmarkWindow = parseStandaloneBookmarkWindowFromUITreeRoot(
    #     uiTree)
    # x.neocom = parseNeocomFromUITreeRoot(uiTree)
    # x.messageBoxes = parseMessageBoxesFromUITreeRoot(uiTree)
    # x.layerAbovemain = parseLayerAbovemainFromUITreeRoot(uiTree)
    # x.keyActivationWindow = parseKeyActivationWindowFromUITreeRoot(uiTree)
    return x


# parseUserinterfaceFromUITree : UITreeNodeWithDisplayRegion -> ParsedUserinterface
# parseUserinterfaceFromUITree uiTree =
#     { uiTree = uiTree
#     , contextMenus = parseContextMenusFromUITreeRoot uiTree
#     , shipUI = parseShipUIFromUITreeRoot uiTree
#     , targets = parseTargetsFromUITreeRoot uiTree
#     , infoPanelContainer = parseInfoPanelContainerFromUIRoot uiTree
#     , overviewWindow = parseOverviewWindowFromUITreeRoot uiTree
#     , selectedItemWindow = parseSelectedItemWindowFromUITreeRoot uiTree
#     , dronesWindow = parseDronesWindowFromUITreeRoot uiTree
#     , fittingWindow = parseFittingWindowFromUITreeRoot uiTree
#     , probeScannerWindow = parseProbeScannerWindowFromUITreeRoot uiTree
#     , directionalScannerWindow = parseDirectionalScannerWindowFromUITreeRoot uiTree
#     , stationWindow = parseStationWindowFromUITreeRoot uiTree
#     , inventoryWindows = parseInventoryWindowsFromUITreeRoot uiTree
#     , moduleButtonTooltip = parseModuleButtonTooltipFromUITreeRoot uiTree
#     , chatWindowStacks = parseChatWindowStacksFromUITreeRoot uiTree
#     , agentConversationWindows = parseAgentConversationWindowsFromUITreeRoot uiTree
#     , marketOrdersWindow = parseMarketOrdersWindowFromUITreeRoot uiTree
#     , surveyScanWindow = parseSurveyScanWindowFromUITreeRoot uiTree
#     , bookmarkLocationWindow = parseBookmarkLocationWindowFromUITreeRoot uiTree
#     , repairShopWindow = parseRepairShopWindowFromUITreeRoot uiTree
#     , characterSheetWindow = parseCharacterSheetWindowFromUITreeRoot uiTree
#     , fleetWindow = parseFleetWindowFromUITreeRoot uiTree
#     , watchListPanel = parseWatchListPanelFromUITreeRoot uiTree
#     , standaloneBookmarkWindow = parseStandaloneBookmarkWindowFromUITreeRoot uiTree
#     , neocom = parseNeocomFromUITreeRoot uiTree
#     , messageBoxes = parseMessageBoxesFromUITreeRoot uiTree
#     , layerAbovemain = parseLayerAbovemainFromUITreeRoot uiTree
#     , keyActivationWindow = parseKeyActivationWindowFromUITreeRoot uiTree
#     }

def unwrapUITreeNodeChild(child: UITreeNodeChild) -> UITreeNode:
    # print("Type of Child :", type(child))
    if type(child) == UITreeNodeChild:
        return child
    # if child is UITreeNodeChild:
    #     return child.

# unwrapUITreeNodeChild : UITreeNodeChild -> UITreeNode
# unwrapUITreeNodeChild child =
#     case child of
#         UITreeNodeChild node ->
#             node


def asUITreeNodeWithDisplayRegion(selfDisplayRegion: DisplayRegion, totalDisplayRegion: DisplayRegion, uiNode: UITreeNode) -> UITreeNodeWithDisplayRegion:
    x = UITreeNodeWithDisplayRegion()
    x.uiNode = uiNode
    dr = Location2d()
    dr.x = totalDisplayRegion.x
    dr.y = totalDisplayRegion.y
    x.children = [asUITreeNodeWithInheritedOffset(dr, unwrapUITreeNodeChild(
        x)) for x in uiNode.children if x is not None] if uiNode.children is not None else None  # TODO: for all children do `unwrapUITreeNodeChild`
    x.selfDisplayRegion = selfDisplayRegion
    x.totalDisplayRegion = totalDisplayRegion
    return x

# asUITreeNodeWithDisplayRegion : { selfDisplayRegion : DisplayRegion, totalDisplayRegion : DisplayRegion } -> UITreeNode -> UITreeNodeWithDisplayRegion
# asUITreeNodeWithDisplayRegion { selfDisplayRegion, totalDisplayRegion } uiNode =
#     { uiNode = uiNode
#     , children = uiNode.children |> Maybe.map (List.map (unwrapUITreeNodeChild >> asUITreeNodeWithInheritedOffset { x = totalDisplayRegion.x, y = totalDisplayRegion.y }))
#     , selfDisplayRegion = selfDisplayRegion
#     , totalDisplayRegion = totalDisplayRegion
#     }


def asUITreeNodeWithInheritedOffset(inheritedOffset: Location2d, rawNode: UITreeNode) -> UITreeNodeWithDisplayRegion:
    selfRegion = getDisplayRegionFromDictEntries(rawNode)
    if selfRegion is None:
        return ChildWithoutRegion(rawNode)
    a = copy(selfRegion)
    a.x += (inheritedOffset.x or 0)
    a.y += (inheritedOffset.y or 0)
    return asUITreeNodeWithDisplayRegion(selfRegion, a, rawNode)


# asUITreeNodeWithInheritedOffset : { x : int, y : int } -> UITreeNode -> ChildOfNodeWithDisplayRegion
# asUITreeNodeWithInheritedOffset inheritedOffset rawNode =
#     case rawNode |> getDisplayRegionFromDictEntries of
#         Nothing ->
#             ChildWithoutRegion rawNode
#         Just selfRegion ->
#             ChildWithRegion
#                 (asUITreeNodeWithDisplayRegion
#                     { selfDisplayRegion = selfRegion
#                     , totalDisplayRegion =
#                         { selfRegion | x = inheritedOffset.x + selfRegion.x, y = inheritedOffset.y + selfRegion.y }
#                     }
#                     rawNode
#                 )


def getDisplayRegionFromDictEntries(uiNode: UITreeNode) -> Optional[DisplayRegion]:
    def fixedNumberFromJsonValue(val: Union[int, str]):
        if type(val) is int:
            return val
        else:
            try:
                # print("Val", val)
                if val is None:
                    return 0
                if type(val) is dict:
                    return int(val.get("int_low32"))
                return int(val)
            except Exception as e:
                print("Excemption Parsing: ", e)
                return None

    def fixedNumberFromPropertyName(name: str) -> int:
        return fixedNumberFromJsonValue(uiNode.dictEntriesOfInterest.get(name))

    dr = DisplayRegion()
    dr.x = fixedNumberFromPropertyName("_displayX")
    dr.y = fixedNumberFromPropertyName("_displayY")
    dr.width = fixedNumberFromPropertyName("_displayWidth")
    dr.height = fixedNumberFromPropertyName("_displayHeight")
    # print("Display Region: ", vars(dr))
    return dr

# getDisplayRegionFromDictEntries : UITreeNode -> Maybe DisplayRegion
# getDisplayRegionFromDictEntries uiNode =
#     let
#         fixedNumberFromJsonValue =
#             Json.Decode.decodeValue
#                 (Json.Decode.oneOf
#                     [ jsonDecodeintFromintOrstr
#                     , Json.Decode.field "int_low32" jsonDecodeintFromintOrstr
#                     ]
#                 )
#         fixedNumberFromPropertyName propertyName =
#             uiNode.dictEntriesOfinterest
#                 |> Dict.get propertyName
#                 |> Maybe.andThen (fixedNumberFromJsonValue >> Result.toMaybe)
#     in
#     case
#         ( ( fixedNumberFromPropertyName "_displayX", fixedNumberFromPropertyName "_displayY" )
#         , ( fixedNumberFromPropertyName "_displayWidth", fixedNumberFromPropertyName "_displayHeight" )
#         )
#     of
#         ( ( Just displayX, Just displayY ), ( Just displayWidth, Just displayHeight ) ) ->
#             Just { x = displayX, y = displayY, width = displayWidth, height = displayHeight }
#         _ ->
#             Nothing


def parseContextMenusFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[ContextMenu]:
    displayRegions = [x for x in listChildrenWithDisplayRegion(
        uiTreeRoot) if getNameFromDictEntries(x.uiNode).lower() == 'l_menu']
    if len(displayRegions) == 0:
        return []
    layerMenu = displayRegions[0]
    return[parseContextMenu(x) for x in listChildrenWithDisplayRegion(layerMenu) if 'menu' in x.uiNode.pythonObjectTypeName.lower()]

# parseContextMenusFromUITreeRoot : UITreeNodeWithDisplayRegion -> List ContextMenu
# parseContextMenusFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listChildrenWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map str.toLower >> (==) (Just "l_menu"))
#             |> List.head
#     of
#         Nothing ->
#             []
#         Just layerMenu ->
#             layerMenu
#                 |> listChildrenWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "menu")
#                 |> List.map parseContextMenu


def parseInfoPanelContainerFromUIRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelContainer]:
    raise NotImplementedError()
# parseContextMenusFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe InfoPanelContainer
# parseInfoPanelContainerFromUIRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelContainer")
#             |> List.sortBy (.uiNode >> countDescendantsInUITreeNode >> negate)
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just containerNode ->
#             Just
#                 { uiNode = containerNode
#                 , icons = parseInfoPanelIconsFromInfoPanelContainer containerNode
#                 , infoPanelLocationInfo = parseInfoPanelLocationInfoFromInfoPanelContainer containerNode
#                 , infoPanelRoute = parseInfoPanelRouteFromInfoPanelContainer containerNode
#                 , infoPanelAgentMissions = parseInfoPanelAgentMissionsFromInfoPanelContainer containerNode
#                 }


def parseInfoPanelIconsFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelIcons]:
    raise NotImplementedError()

# parseInfoPanelIconsFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelIcons
# parseInfoPanelIconsFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "iconCont") >> Maybe.withDefault False)
#             |> List.sortBy (.totalDisplayRegion >> .y)
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just iconContainerNode ->
#             let
#                 iconNodeFromTexturePathEnd texturePathEnd =
#                     iconContainerNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter
#                             (.uiNode
#                                 >> getTexturePathFromDictEntries
#                                 >> Maybe.map (str.endsWith texturePathEnd)
#                                 >> Maybe.withDefault False
#                             )
#                         |> List.head
#             in
#             Just
#                 { uiNode = iconContainerNode
#                 , search = iconNodeFromTexturePathEnd "search.png"
#                 , locationInfo = iconNodeFromTexturePathEnd "LocationInfo.png"
#                 , route = iconNodeFromTexturePathEnd "Route.png"
#                 , agentMissions = iconNodeFromTexturePathEnd "Missions.png"
#                 , dailyChallenge = iconNodeFromTexturePathEnd "dailyChallenge.png"
#                 }


def parseInfoPanelLocationInfoFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelLocationInfo]:
    raise NotImplementedError()
# parseInfoPanelLocationInfoFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelLocationInfo
# parseInfoPanelLocationInfoFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelLocationInfo")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelNode ->
#             let
#                 securityStatusPercent =
#                     infoPanelNode.uiNode
#                         |> getAllContainedDisplayTexts
#                         |> List.filterMap parseSecurityStatusPercentFromUINodeText
#                         |> List.head
#                 currentSolarSystemName =
#                     infoPanelNode.uiNode
#                         |> getAllContainedDisplayTexts
#                         |> List.filterMap parseCurrentSolarSystemFromUINodeText
#                         |> List.head
#                         |> Maybe.map str.trim
#                 maybeListSurroundingsButton =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ListSurroundingsBtn")
#                         |> List.head
#                 expandedContent =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter
#                             (\uiNode ->
#                                 (uiNode.uiNode.pythonObjectTypeName |> str.contains "Container")
#                                     && (uiNode.uiNode |> getNameFromDictEntries |> Maybe.withDefault "" |> str.contains "mainCont")
#                             )
#                         |> List.head
#                         |> Maybe.map
#                             (\expandedContainer ->
#                                 { currentStationName =
#                                     expandedContainer.uiNode
#                                         |> getAllContainedDisplayTexts
#                                         |> List.filterMap parseCurrentStationNameFromInfoPanelLocationInfoLabelText
#                                         |> List.head
#                                 }
#                             )
#             in
#             maybeListSurroundingsButton
#                 |> Maybe.map
#                     (\listSurroundingsButton ->
#                         { uiNode = infoPanelNode
#                         , listSurroundingsButton = listSurroundingsButton
#                         , currentSolarSystemName = currentSolarSystemName
#                         , securityStatusPercent = securityStatusPercent
#                         , expandedContent = expandedContent
#                         }
#                     )


def parseSecurityStatusPercentFromUINodeText(s: str) -> Optional[int]:
    raise NotImplementedError()
# parseSecurityStatusPercentFromUINodeText : str -> Maybe int
# parseSecurityStatusPercentFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "hint='Security status'"
#         , getSubstrBetweenXmlTagsAfterMarker "hint=\"Security status\"><color="
#         ]
#         >> Maybe.andThen (str.trim >> str.toFloat)
#         >> Maybe.map ((*) 100 >> round)


def parseCurrentSolarSystemFromUINodeText(s: str) -> Optional[str]:
    raise NotImplementedError()
# parseCurrentSolarSystemFromUINodeText : str -> Maybe str
# parseCurrentSolarSystemFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "alt='Current Solar System'"
#         , getSubstrBetweenXmlTagsAfterMarker "alt=\"Current Solar System\""
#         ]


def parseCurrentStationNameFromInfoPanelLocationInfoLabelText(s: str) -> Optional[str]:
    raise NotImplementedError()
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText : str -> Maybe str
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText =
#     getSubstrBetweenXmlTagsAfterMarker "alt='Current Station'"
#         >> Maybe.map str.trim


def parseInfoPanelRouteFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelRoute]:
    raise NotImplementedError()
# parseInfoPanelRouteFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelRoute
# parseInfoPanelRouteFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelRoute")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelRouteNode ->
#             let
#                 routeElementMarker =
#                     infoPanelRouteNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AutopilotDestinationIcon")
#                         |> List.map (\uiNode -> { uiNode = uiNode })
#             in
#             Just { uiNode = infoPanelRouteNode, routeElementMarker = routeElementMarker }


def parseInfoPanelAgentMissionsFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelAgentMissions]:
    raise NotImplementedError()
# parseInfoPanelAgentMissionsFromInfoPanelContainer : UITreeNodeWithDisplayRegion -> Maybe InfoPanelAgentMissions
# parseInfoPanelAgentMissionsFromInfoPanelContainer infoPanelContainerNode =
#     case
#         infoPanelContainerNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InfoPanelAgentMissions")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just infoPanelNode ->
#             let
#                 entries =
#                     infoPanelNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MissionEntry")
#                         |> List.map (\uiNode -> { uiNode = uiNode })
#             in
#             Just
#                 { uiNode = infoPanelNode
#                 , entries = entries
#                 }


def parseContextMenu(contextMenuUINode: UITreeNodeWithDisplayRegion) -> ContextMenu:
    entriesUINodes = [x for x in listDescendantsWithDisplayRegion(
        contextMenuUINode) if 'menuentry' in x.uiNode.pythonObjectTypeName.lower()]
    entries = []
    for entryUiNode in entriesUINodes:
        texts = [getDisplayText(x.uiNode)
                 for x in listDescendantsWithDisplayRegion(entryUiNode)]
        texts.sort(key=len, reverse=True)  # negate?
        entry = ContextMenuEntry()
        entry.text = texts[0] if len(texts) > 0 else ''
        entry.uiNode = entryUiNode
        entries.append(entry)
    result = ContextMenu()
    result.entries = entries
    result.uiNode = contextMenuUINode
    return result

# parseContextMenu : UITreeNodeWithDisplayRegion -> ContextMenu
# parseContextMenu contextMenuUINode =
#     let
#         entriesUINodes =
#             contextMenuUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "menuentry")
#         entries =
#             entriesUINodes
#                 |> List.map
#                     (\entryUINode ->
#                         let
#                             text =
#                                 entryUINode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filterMap (.uiNode >> getDisplayText)
#                                     |> List.sortBy (str.length >> negate)
#                                     |> List.head
#                                     |> Maybe.withDefault ""
#                         in
#                         { text = text
#                         , uiNode = entryUINode
#                         }
#                     )
#                 |> List.sortBy (.uiNode >> .totalDisplayRegion >> .y)
#     in
#     { uiNode = contextMenuUINode
#     , entries = entries
#     }


def parseShipUIFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ShipUI]:
    displays = [x for x in listDescendantsWithDisplayRegion(
        uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'ShipUI']
    if len(displays) == 0:
        return None
    shipUINode = displays[0]
    uiNodes = [x for x in listDescendantsWithDisplayRegion(
        shipUINode) if x.uiNode.pythonObjectTypeName == 'CapacitorContainer']
    if len(uiNodes) == 0:
        return None
    capacitorUINode = uiNodes[0]

    def descendantNodesFromPythonObjectTypeNameEqual(pythonObjectTypeName: str):
        return [x for x in listDescendantsWithDisplayRegion(shipUINode) if x.uiNode.pythonObjectTypeName == pythonObjectTypeName]
    capacitor = parseShipUICapacitorFromUINode(capacitorUINode)

    speedGaugeElement = [x for x in listDescendantsWithDisplayRegion(
        shipUINode) if x.uiNode.pythonObjectTypeName == 'SpeedGauge']
    if len(speedGaugeElement) == 0:
        return None
    speedGaugeElement = speedGaugeElement[0]
    maybeIndicationNode = [x for x in listDescendantsWithDisplayRegion(
        shipUINode) if 'indicationcontainer' in (getNameFromDictEntries(x.uiNode) or '').lower()][0]
    indication = parseShipUIIndication(maybeIndicationNode) or None
    decendants = [x for x in listDescendantsWithDisplayRegion(shipUINode) if x.uiNode.pythonObjectTypeName == 'ShipSlot']
    modulebuttons = []
    for slotNode in decendants:
        moduleButtonNode = [x for x in listDescendantsWithDisplayRegion(slotNode) if x.uiNode.pythonObjectTypeName == 'ModuleButton'][0]
        modulebuttons.append(parseShipUIModuleButton(slotNode, moduleButtonNode))
    def getLastValuePercentFromGaugeName(gaugeName):
        options = [x for x in listDescendantsWithDisplayRegion(shipUINode) if getNameFromDictEntries(x.uiNode) == gaugeName]
        if len(options) == 0: return None
        option = options[0].uiNode.dictEntriesOfInterest.get('_lastValue')
        if option: option = float(option)
        option = round(option * 100)
        return option
    maybeHitpointsPercent = Hitpoints()
    maybeHitpointsPercent.armor = getLastValuePercentFromGaugeName('armorGauge')
    maybeHitpointsPercent.structure = getLastValuePercentFromGaugeName('structureGauge')
    maybeHitpointsPercent.shield = getLastValuePercentFromGaugeName('shieldGauge')
    offensiveBuffButtonNames = [x for x in listDescendantsWithDisplayRegion(shipUINode) if x.uiNode.pythonObjectTypeName == 'OffensiveBuffButton']
    # and getNameFromDictEntries(.uiNode)
    _squadronsUI = [parseSquadronsUI(x) for x in listDescendantsWithDisplayRegion(shipUINode) if x.uiNode.pythonObjectTypeName == 'SquadronsUI']
    squadronsUI = None if len(_squadronsUI) == 0 else squadronsUI[0]
    data = ShipUI()
    data.uiNode = shipUINode
    data.capacitor = capacitor
    data.hitpointsPercent = maybeHitpointsPercent
    data.indication = indication
    data.moduleButtons = modulebuttons
    data.moduleButtonsRows = groupShipUIModulesintoRows(capacitor, modulebuttons)
    data.offensiveBuffButtonNames = offensiveBuffButtonNames
    data.squadronsUI = squadronsUI
    data.stopButton = descendantNodesFromPythonObjectTypeNameEqual("StopButton")[0]
    data.maxSpeedButton = descendantNodesFromPythonObjectTypeNameEqual("MaxSpeedButton")[0]
    return data




    
# parseShipUIFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ShipUI
# parseShipUIFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ShipUI")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just shipUINode ->
#             case
#                 shipUINode
#                     |> listDescendantsWithDisplayRegion
#                     |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "CapacitorContainer")
#                     |> List.head
#             of
#                 Nothing ->
#                     Nothing
#                 Just capacitorUINode ->
#                     let
#                         descendantNodesFromPythonObjectTypeNameEqual pythonObjectTypeName =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) pythonObjectTypeName)
#                         capacitor =
#                             capacitorUINode |> parseShipUICapacitorFromUINode
#                         {-
#                            speedGaugeElement =
#                                shipUINode
#                                    |> listDescendantsWithDisplayRegion
#                                    |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SpeedGauge")
#                                    |> List.head
#                         -}
#                         maybeIndicationNode =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "indicationcontainer") >> Maybe.withDefault False)
#                                 |> List.head
#                         indication =
#                             maybeIndicationNode
#                                 |> Maybe.map (parseShipUIIndication >> Just)
#                                 |> Maybe.withDefault Nothing
#                         moduleButtons =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ShipSlot")
#                                 |> List.filterMap
#                                     (\slotNode ->
#                                         slotNode
#                                             |> listDescendantsWithDisplayRegion
#                                             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ModuleButton")
#                                             |> List.head
#                                             |> Maybe.map
#                                                 (\moduleButtonNode ->
#                                                     parseShipUIModuleButton { slotNode = slotNode, moduleButtonNode = moduleButtonNode }
#                                                 )
#                                     )
#                         getLastValuePercentFromGaugeName gaugeName =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) gaugeName) >> Maybe.withDefault False)
#                                 |> List.head
#                                 |> Maybe.andThen (.uiNode >> .dictEntriesOfinterest >> Dict.get "_lastValue")
#                                 |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#                                 |> Maybe.map ((*) 100 >> round)
#                         maybeHitpointsPercent =
#                             case ( getLastValuePercentFromGaugeName "structureGauge", getLastValuePercentFromGaugeName "armorGauge", getLastValuePercentFromGaugeName "shieldGauge" ) of
#                                 ( Just structure, Just armor, Just shield ) ->
#                                     Just { structure = structure, armor = armor, shield = shield }
#                                 _ ->
#                                     Nothing
#                         offensiveBuffButtonNames =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OffensiveBuffButton")
#                                 |> List.filterMap (.uiNode >> getNameFromDictEntries)
#                         squadronsUI =
#                             shipUINode
#                                 |> listDescendantsWithDisplayRegion
#                                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronsUI")
#                                 |> List.head
#                                 |> Maybe.map parseSquadronsUI
#                     in
#                     maybeHitpointsPercent
#                         |> Maybe.map
#                             (\hitpointsPercent ->
#                                 { uiNode = shipUINode
#                                 , capacitor = capacitor
#                                 , hitpointsPercent = hitpointsPercent
#                                 , indication = indication
#                                 , moduleButtons = moduleButtons
#                                 , moduleButtonsRows = groupShipUIModulesintoRows capacitor moduleButtons
#                                 , offensiveBuffButtonNames = offensiveBuffButtonNames
#                                 , squadronsUI = squadronsUI
#                                 , stopButton = descendantNodesFromPythonObjectTypeNameEqual "StopButton" |> List.head
#                                 , maxSpeedButton = descendantNodesFromPythonObjectTypeNameEqual "MaxSpeedButton" |> List.head
#                                 }
#                             )


def parseShipUIModuleButton(slotNode: UITreeNodeWithDisplayRegion, moduleButtonNode: UITreeNodeWithDisplayRegion) -> ShipUIModuleButton:
    print("SlotNode: ", slotNode)
    def rotationFloatFromRampName(rampName: str) -> Optional[float]:
        _data = [getRotationFloatFromDictEntries(x.uiNode) for x in listDescendantsWithDisplayRegion(slotNode) if rampName in (getNameFromDictEntries(x.uiNode) or [])]
        return _data[0] if len(_data)>0 else None
    leftRampRotationFloat = rotationFloatFromRampName("leftRamp") or 0    # A Default Vaule if there is no LeftRamp
    rightRampRotationFloat = rotationFloatFromRampName("rightRamp") or 0  # A Default Vaule if there is no LeftRamp
    rampRotationMilli = None if (leftRampRotationFloat<0 or pi * 2.01 < leftRampRotationFloat) or (rightRampRotationFloat<0 or pi * 2.01 < rightRampRotationFloat) else max(0, min(1000, round(1000 - ((leftRampRotationFloat + rightRampRotationFloat) * 500 ) / pi)))
    result = ShipUIModuleButton()
    result.uiNode = moduleButtonNode
    result.slotUINode = slotNode
    result.isActive = "ramp_active" in  moduleButtonNode.uiNode.dictEntriesOfInterest
    result.isHiliteVisible = len([x for x in listDescendantsWithDisplayRegion(slotNode) if "Sprite" in x.uiNode.pythonObjectTypeName and 'hilite' in getNameFromDictEntries(x.uiNode) ]) > 0
    result.rampRotationMilli = rampRotationMilli
    return result

# parseShipUIModuleButton : { slotNode : UITreeNodeWithDisplayRegion, moduleButtonNode : UITreeNodeWithDisplayRegion } -> ShipUIModuleButton
# parseShipUIModuleButton { slotNode, moduleButtonNode } =
#     let
#         rotationFloatFromRampName rampName =
#             slotNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just rampName))
#                 |> List.filterMap (.uiNode >> getRotationFloatFromDictEntries)
#                 |> List.head
#         rampRotationMilli =
#             case ( rotationFloatFromRampName "leftRamp", rotationFloatFromRampName "rightRamp" ) of
#                 ( Just leftRampRotationFloat, Just rightRampRotationFloat ) ->
#                     if
#                         (leftRampRotationFloat < 0 || pi * 2.01 < leftRampRotationFloat)
#                             || (rightRampRotationFloat < 0 || pi * 2.01 < rightRampRotationFloat)
#                     then
#                         Nothing
#                     else
#                         Just (max 0 (min 1000 (round (1000 - ((leftRampRotationFloat + rightRampRotationFloat) * 500) / pi))))
#                 _ ->
#                     Nothing
#     in
#     { uiNode = moduleButtonNode
#     , slotUINode = slotNode
#     , isActive =
#         moduleButtonNode.uiNode.dictEntriesOfinterest
#             |> Dict.get "ramp_active"
#             |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.bool >> Result.toMaybe)
#     , isHiliteVisible =
#         slotNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Sprite")
#             |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "hilite"))
#             |> List.isEmpty
#             |> not
#     , rampRotationMilli = rampRotationMilli
#     }


def parseShipUICapacitorFromUINode(capacitorUINode: UITreeNodeWithDisplayRegion) -> ShipUICapacitor:
    pmarks = [ShipUICapacitorPmark(uiNode=x, colorPercent=getColorPercentFromDictEntries(x.uiNode)) for x in listDescendantsWithDisplayRegion(capacitorUINode) if getNameFromDictEntries(x.uiNode) == 'pmark']
    _maybePmarksFills = [ x.colorPercent if x.colorPercent.a < 20 else None for x in pmarks ]
    maybePmarksFills = _maybePmarksFills if None not in _maybePmarksFills else None
    levelFromPmarksPercent = None
    if maybePmarksFills is not None:
        pmarksFills = maybePmarksFills
        if len(pmarksFills) == 0: 
            levelFromPmarksPercent = None
        else:
            levelFromPmarksPercent = len(pmarksFills) * 100 // len(pmarksFills)
    result = ShipUICapacitor()
    result.uiNode = capacitorUINode
    result.pmarks = pmarks
    result.levelFromPmarksPercent = levelFromPmarksPercent
    return result


# parseShipUICapacitorFromUINode : UITreeNodeWithDisplayRegion -> ShipUICapacitor
# parseShipUICapacitorFromUINode capacitorUINode =
#     let
#         pmarks =
#             capacitorUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "pmark") >> Maybe.withDefault False)
#                 |> List.map
#                     (\pmarkUINode ->
#                         { uiNode = pmarkUINode
#                         , colorPercent = pmarkUINode.uiNode |> getColorPercentFromDictEntries
#                         }
#                     )
#         maybePmarksFills =
#             pmarks
#                 |> List.map (.colorPercent >> Maybe.map (\colorPercent -> colorPercent.a < 20))
#                 |> Maybe.Extra.combine # None or list.
#         levelFromPmarksPercent =
#             maybePmarksFills
#                 |> Maybe.andThen
#                     (\pmarksFills ->
#                         if (pmarksFills |> List.length) < 1 then
#                             Nothing
#                         else
#                             Just (((pmarksFills |> List.filter identity |> List.length) * 100) // (pmarksFills |> List.length))
#                     )
#     in
#     { uiNode = capacitorUINode
#     , pmarks = pmarks
#     , levelFromPmarksPercent = levelFromPmarksPercent
#     }


def groupShipUIModulesintoRows(capacitor: ShipUICapacitor, modules: List[ShipUIModuleButton]) -> ModuleRows:

    verticalDistanceThreshold = 20

    def verticalCenterOfUINode(uiNode: UITreeNodeWithDisplayRegion) -> int:
        print("Y: ", uiNode.totalDisplayRegion.y)
        print("Height: ", uiNode.totalDisplayRegion.height)
        return uiNode.totalDisplayRegion.y + (uiNode.totalDisplayRegion.height // 2)
    capacitorVerticalCenter = verticalCenterOfUINode(capacitor.uiNode)

    def foldFunction(shipModule: ShipUIModuleButton, previousRows: ModuleRows):
        print("Previous Rows", previousRows)
        verticalCenter = verticalCenterOfUINode(shipModule.uiNode)
        print("verticalCenter", verticalCenter, "<", (capacitorVerticalCenter - verticalDistanceThreshold), ">", (capacitorVerticalCenter + verticalDistanceThreshold))
        if verticalCenter < (capacitorVerticalCenter - verticalDistanceThreshold):
            previousRows.top.append(shipModule)
        elif verticalCenter > (capacitorVerticalCenter + verticalDistanceThreshold):
            previousRows.bottom.append(shipModule)
        else:
            previousRows.middle.append(shipModule)
        return previousRows
    _modules = ModuleRows(top=[], middle=[], bottom=[])
    # print([x for x in modules])
    print("Modules ", _modules)
    result: ModuleRows = foldr(foldFunction, _modules, modules)
    print("Response", len(result.top), len(result.middle), len(result.bottom))
    return result
# groupShipUIModulesintoRows :
#     ShipUICapacitor
#     -> List ShipUIModuleButton
#     -> { top : List ShipUIModuleButton, middle : List ShipUIModuleButton, bottom : List ShipUIModuleButton }
# groupShipUIModulesintoRows capacitor modules =
#     let
#         verticalDistanceThreshold =
#             20
#         verticalCenterOfUINode uiNode =
#             uiNode.totalDisplayRegion.y + uiNode.totalDisplayRegion.height // 2
#         capacitorVerticalCenter =
#             verticalCenterOfUINode capacitor.uiNode
#     in
#     modules
#         |> List.foldr
#             (\shipModule previousRows ->
#                 if verticalCenterOfUINode shipModule.uiNode < capacitorVerticalCenter - verticalDistanceThreshold then
#                     { previousRows | top = shipModule :: previousRows.top }
#                 else if verticalCenterOfUINode shipModule.uiNode > capacitorVerticalCenter + verticalDistanceThreshold then
#                     { previousRows | bottom = shipModule :: previousRows.bottom }
#                 else
#                     { previousRows | middle = shipModule :: previousRows.middle }
#             )
#             { top = [], middle = [], bottom = [] }


def parseShipUIIndication(indicationUINode: UITreeNodeWithDisplayRegion) -> ShipUIIndication:
    displayTexts = getAllContainedDisplayTexts(indicationUINode.uiNode)
    _maneuvertype = [ candidateManeuverType for  pattern, candidateManeuverType in [
            ("Warp", ShipManeuverType.ManeuverWarp),
            ("Jump", ShipManeuverType.ManeuverJump),
            ("Orbit", ShipManeuverType.ManeuverOrbit),
            ("Approach", ShipManeuverType.ManeuverApproach)
        ] if pattern in displayTexts
    ]
    maneuvertype = _maneuvertype[0] if len(_maneuvertype) > 0 else None
    result = ShipUIIndication()
    result.maneuverType = maneuvertype
    result.uiNode = indicationUINode
    return result

# parseShipUIIndication : UITreeNodeWithDisplayRegion -> ShipUIIndication
# parseShipUIIndication indicationUINode =
#     let
#         displayTexts =
#             indicationUINode.uiNode |> getAllContainedDisplayTexts
#         maneuverType =
#             [ ( "Warp", ManeuverWarp )
#             , ( "Jump", ManeuverJump )
#             , ( "Orbit", ManeuverOrbit )
#             , ( "Approach", ManeuverApproach )
#             -- Sample `session-2022-05-23T23-00-32-87ba97.zip` shared by Abaddon at https://forum.botlab.org/t/i-want-to-add-korean-support-on-eve-online-bot-what-should-i-do/4370/9
#             , ( "?????? ???????????? ??????", ManeuverWarp )
#             -- Sample `session-2022-05-26T03-13-42-83df2b.zip` shared by Abaddon at https://forum.botlab.org/t/i-want-to-add-korean-support-on-eve-online-bot-what-should-i-do/4370/14
#             , ( "?????? ???", ManeuverJump )
#             ]
#                 |> List.filterMap
#                     (\( pattern, candidateManeuverType ) ->
#                         if displayTexts |> List.any (str.contains pattern) then
#                             Just candidateManeuverType
#                         else
#                             Nothing
#                     )
#                 |> List.head
#     in
#     { uiNode = indicationUINode, maneuverType = maneuverType }


def parseSquadronsUI(squadronsUINode: UITreeNodeWithDisplayRegion) -> SquadronsUI:
    raise NotImplementedError()
# parseSquadronsUI : UITreeNodeWithDisplayRegion -> SquadronsUI
# parseSquadronsUI squadronsUINode =
#     { uiNode = squadronsUINode
#     , squadrons =
#         squadronsUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronUI")
#             |> List.map parseSquadronUI
#     }


def parseSquadronUI(squadronUINode: UITreeNodeWithDisplayRegion) -> SquadronUI:
    raise NotImplementedError()
# parseSquadronUI : UITreeNodeWithDisplayRegion -> SquadronUI
# parseSquadronUI squadronUINode =
#     { uiNode = squadronUINode
#     , abilities =
#         squadronUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AbilityIcon")
#             |> List.map parseSquadronAbilityIcon
#     , actionLabel =
#         squadronUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronActionLabel")
#             |> List.head
#     }


def parseSquadronAbilityIcon(abilityIconUINode: UITreeNodeWithDisplayRegion) -> SquadronAbilityIcon:
    raise NotImplementedError()
# parseSquadronAbilityIcon : UITreeNodeWithDisplayRegion -> SquadronAbilityIcon
# parseSquadronAbilityIcon abilityIconUINode =
#     { uiNode = abilityIconUINode
#     , quantity =
#         abilityIconUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "quantity") >> Maybe.withDefault False)
#             |> List.concatMap (.uiNode >> getAllContainedDisplayTexts)
#             |> List.head
#             |> Maybe.andThen (str.trim >> str.toint)
#     , ramp_active =
#         abilityIconUINode.uiNode.dictEntriesOfinterest
#             |> Dict.get "ramp_active"
#             |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.bool >> Result.toMaybe)
#     }


def parseTargetsFromUITreeRoot(x: UITreeNodeWithDisplayRegion) -> List[Target]:
    return [parseTarget(y) for y in listDescendantsWithDisplayRegion(x) if y.uiNode.pythonObjectTypeName == 'TargetInBar']
# parseTargetsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List Target
# parseTargetsFromUITreeRoot =
#     listDescendantsWithDisplayRegion
#         >> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "TargetInBar")
#         >> List.map parseTarget


def parseTarget(targetNode: UITreeNodeWithDisplayRegion) -> Target:
    textsTopToBottom = getAllContainedDisplayTextsWithRegion(targetNode)
    textsTopToBottom.sort( key=lambda x: x[1].totalDisplayRegion.y)
    textsTopToBottom = [x[0] for x in textsTopToBottom]
    barAndImageCont = [x for x in listDescendantsWithDisplayRegion(targetNode) if getNameFromDictEntries(x.uiNode) == 'barAndImageCont'][0]
    isActiveTarget = [x for x in listDescendantsInUITreeNode(targetNode.uiNode) if x.pythonObjectTypeName == 'ActiveTargetOnBracket']
    assignedContainerNode = [x for x in listDescendantsWithDisplayRegion(targetNode) if 'assigned' in getNameFromDictEntries(x.uiNode).lower() ]
    assignedContainerNode.sort( key = lambda x: x.totalDisplayRegion.width)
    assignedContainerNode = assignedContainerNode[0]

    assignedIcons = [x for x in listDescendantsWithDisplayRegion(assignedContainerNode) if x.uiNode.pythonObjectTypeName in ['Icon', 'Sprite']]

    result = Target()
    result.assignedContainerNode = assignedContainerNode
    result.assignedIcons = assignedIcons
    result.barAndImageCont = barAndImageCont
    result.isActiveTarget = isActiveTarget
    result.textsTopToBottom = textsTopToBottom
    result.uiNode = targetNode
    return result
# parseTarget : UITreeNodeWithDisplayRegion -> Target
# parseTarget targetNode =
#     let
#         textsTopToBottom =
#             targetNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .y)
#                 |> List.map Tuple.first
#         barAndImageCont =
#             targetNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "barAndImageCont"))
#                 |> List.head
#         isActiveTarget =
#             targetNode.uiNode
#                 |> listDescendantsInUITreeNode
#                 |> List.any (.pythonObjectTypeName >> (==) "ActiveTargetOnBracket")
#         assignedContainerNode =
#             targetNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "assigned") >> Maybe.withDefault False)
#                 |> List.sortBy (.totalDisplayRegion >> .width)
#                 |> List.head
#         assignedIcons =
#             assignedContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (\uiNode -> [ "Sprite", "Icon" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#     in
#     { uiNode = targetNode
#     , barAndImageCont = barAndImageCont
#     , textsTopToBottom = textsTopToBottom
#     , isActiveTarget = isActiveTarget
#     , assignedContainerNode = assignedContainerNode
#     , assignedIcons = assignedIcons
#     }


def parseOverviewWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[OverviewWindow]:
    data = [ x for x in listDescendantsWithDisplayRegion(uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'OverView']
    if len(data) == 0: return None
    overviewWindowNode = data[0]
    scrollNode = [x for x in listDescendantsWithDisplayRegion(overviewWindowNode) if "scroll" in x.uiNode.pythonObjectTypeName.lower()][0]

    for _node in listDescendantsWithDisplayRegion(scrollNode):
        if "ScrollControls" in _node.uiNode.pythonObjectTypeName:
            scrollControlsNode = _node
            continue
        if "scroll" in _node.uiNode.pythonObjectTypeName.lower():
            headersContrainerNode = _node
            continue
    entriesHeaders = [x for x in listDescendantsWithDisplayRegion(headersContrainerNode) if "headers" in x.uiNode.pythonObjectTypeName.lower()][0]
    entries = [parseOverviewWindowEntry(entriesHeaders, x) for x in listDescendantsWithDisplayRegion(overviewWindowNode) if x.uiNode.pythonObjectTypeName == 'OverviewScrollEntry']

    x = OverviewWindow()
    x.entries = entries
    x.entriesHeaders = entriesHeaders
    x.scrollControls = parseScrollControls(scrollControlsNode) if scrollControlsNode is not None else None
    x.uiNode = overviewWindowNode
    return x
    

# parseOverviewWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe OverviewWindow
# parseOverviewWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OverView")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just overviewWindowNode ->
#             let
#                 scrollNode =
#                     overviewWindowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.head
#                 scrollControlsNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                         |> List.head
#                 headersContainerNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "headers")
#                         |> List.head
#                 entriesHeaders =
#                     headersContainerNode
#                         |> Maybe.map getAllContainedDisplayTextsWithRegion
#                         |> Maybe.withDefault []
#                 entries =
#                     overviewWindowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "OverviewScrollEntry")
#                         |> List.map (parseOverviewWindowEntry entriesHeaders)
#             in
#             Just
#                 { uiNode = overviewWindowNode
#                 , entriesHeaders = entriesHeaders
#                 , entries = entries
#                 , scrollControls = scrollControlsNode |> Maybe.map parseScrollControls
#                 }


def parseOverviewWindowEntry(entriesHeaders: List[Tuple[str, UITreeNodeWithDisplayRegion]], overviewEntryNode: UITreeNodeWithDisplayRegion) -> OverviewWindowEntry:
    textsLeftToRight = [x for x in getAllContainedDisplayTextsWithRegion(overviewEntryNode)]
    textsLeftToRight.sort(key= lambda x: x[1].totalDisplayRegion.x)
    textsLeftToRight = [x[0] for x in textsLeftToRight]
    cellsTexts = []
    for cellText, cell in getAllContainedDisplayTextsWithRegion(overviewEntryNode):
        cellMiddle = cell.totalDisplayRegion.x + (cell.totalDisplayRegion.width // 2)
        maybeHeader = [header for _, header in entriesHeaders if (header.totalDisplayRegion.x < cellMiddle + 1) and (cellMiddle < (header.totalDisplayRegion.x + header.totalDisplayRegion.width -1))]
        cellsTexts.append( [(headerText, cellText) for headerText, _ in maybeHeader])
    cellsTexts = {x:y for x,y in cellsTexts}
    objectDistance = cellsTexts.get("Distance")
    try:
        objectDistanceInMeters = parseOverviewEntryDistanceInMetersFromText(objectDistance)
    except:
        pass
    spaceObjectIconNode = [x for x in listDescendantsWithDisplayRegion(overviewEntryNode) if x.uiNode.pythonObjectTypeName == 'SpaceObjectIcon'][0]
    iconSpriteColorPercent = [getColorPercentFromDictEntries(x.uiNode) for x in listChildrenWithDisplayRegion(overviewEntryNode) if getNameFromDictEntries(x.uiNode) == 'iconSprite']
    namesUnderSpaceObjectIcon = {getNameFromDictEntries(x) for x in listDescendantsInUITreeNode(spaceObjectIconNode.uiNode)}
    bgColorFillsPercent = [getColorPercentFromDictEntries(x.uiNode) for x in listDescendantsWithDisplayRegion(overviewEntryNode) if x.uiNode.pythonObjectTypeName == 'Fill' and getNameFromDictEntries(x.uiNode) == 'bgColor']
    rightAlignedIconsHints = {getHintTextFromDictEntries(y.uiNode).lower() for x in listDescendantsWithDisplayRegion(overviewEntryNode)  for y in listDescendantsWithDisplayRegion(x) if getNameFromDictEntries(x.uiNode) == 'rightAlignedIconContainer'}
    def rightAlignedIconsHintsContainsTextIgnoringCase(textToSearch: str) -> bool:
        return textToSearch.lower() in rightAlignedIconsHints
    result = OverviewWindowEntry()
    commonIndications = OverviewWindowEntryCommonIndications()
    commonIndications.targeting = "targeting" in namesUnderSpaceObjectIcon
    commonIndications.targetedByMe = "targetedByMeIndicator" in namesUnderSpaceObjectIcon
    commonIndications.isJammingMe = rightAlignedIconsHintsContainsTextIgnoringCase("is jamming me")
    commonIndications.isWarpDisruptingMe = rightAlignedIconsHintsContainsTextIgnoringCase("is warp disrupting me")

    result.uiNode = overviewEntryNode
    result.textsLeftToRight = textsLeftToRight
    result.cellsTexts = cellsTexts
    result.objectDistance = objectDistance
    result.objectDistanceInMeters = objectDistanceInMeters
    result.objectName = cellsTexts.get("Name")
    result.objectType = cellsTexts.get("Type")
    result.objectAlliance = cellsTexts.get("Alliance")
    result.iconSpriteColorPercent = iconSpriteColorPercent
    result.namesUnderSpaceObjectIcon = namesUnderSpaceObjectIcon
    result.bgColorFillsPercent = bgColorFillsPercent
    result.rightAlignedIconsHints = rightAlignedIconsHints
    result.commonIndications = commonIndications
    return result

# parseOverviewWindowEntry : List ( str, UITreeNodeWithDisplayRegion ) -> UITreeNodeWithDisplayRegion -> OverviewWindowEntry
# parseOverviewWindowEntry entriesHeaders overviewEntryNode =
#     let
#         textsLeftToRight =
#             overviewEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .x)
#                 |> List.map Tuple.first
#         cellsTexts =
#             overviewEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.filterMap
#                     (\( cellText, cell ) ->
#                         let
#                             cellMiddle =
#                                 cell.totalDisplayRegion.x + (cell.totalDisplayRegion.width // 2)
#                             maybeHeader =
#                                 entriesHeaders
#                                     |> List.filter
#                                         (\( _, header ) ->
#                                             header.totalDisplayRegion.x
#                                                 < cellMiddle
#                                                 + 1
#                                                 && cellMiddle
#                                                 < header.totalDisplayRegion.x
#                                                 + header.totalDisplayRegion.width
#                                                 - 1
#                                         )
#                                     |> List.head
#                         in
#                         maybeHeader
#                             |> Maybe.map (\( headerText, _ ) -> ( headerText, cellText ))
#                     )
#                 |> Dict.fromList
#         objectDistance =
#             cellsTexts
#                 |> Dict.get "Distance"
#         objectDistanceInMeters =
#             objectDistance
#                 |> Maybe.map parseOverviewEntryDistanceInMetersFromText
#                 |> Maybe.withDefault (Err "Did not find the 'Distance' cell text.")
#         spaceObjectIconNode =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SpaceObjectIcon")
#                 |> List.head
#         iconSpriteColorPercent =
#             spaceObjectIconNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "iconSprite"))
#                 |> List.head
#                 |> Maybe.andThen (.uiNode >> getColorPercentFromDictEntries)
#         namesUnderSpaceObjectIcon =
#             spaceObjectIconNode
#                 |> Maybe.map (.uiNode >> listDescendantsInUITreeNode)
#                 |> Maybe.withDefault []
#                 |> List.filterMap getNameFromDictEntries
#                 |> Set.fromList
#         bgColorFillsPercent =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Fill")
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "bgColor") >> Maybe.withDefault False)
#                 |> List.filterMap (\fillUiNode -> fillUiNode.uiNode |> getColorPercentFromDictEntries)
#         rightAlignedIconsHints =
#             overviewEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "rightAlignedIconContainer") >> Maybe.withDefault False)
#                 |> List.concatMap listDescendantsWithDisplayRegion
#                 |> List.filterMap (.uiNode >> getHintTextFromDictEntries)
#         rightAlignedIconsHintsContainsTextIgnoringCase textToSearch =
#             rightAlignedIconsHints |> List.any (str.toLower >> str.contains (textToSearch |> str.toLower))
#         commonIndications =
#             { targeting = namesUnderSpaceObjectIcon |> Set.member "targeting"
#             , targetedByMe = namesUnderSpaceObjectIcon |> Set.member "targetedByMeIndicator"
#             , isJammingMe = rightAlignedIconsHintsContainsTextIgnoringCase "is jamming me"
#             , isWarpDisruptingMe = rightAlignedIconsHintsContainsTextIgnoringCase "is warp disrupting me"
#             }
#     in
#     { uiNode = overviewEntryNode
#     , textsLeftToRight = textsLeftToRight
#     , cellsTexts = cellsTexts
#     , objectDistance = objectDistance
#     , objectDistanceInMeters = objectDistanceInMeters
#     , objectName = cellsTexts |> Dict.get "Name"
#     , objectType = cellsTexts |> Dict.get "Type"
#     , objectAlliance = cellsTexts |> Dict.get "Alliance"
#     , iconSpriteColorPercent = iconSpriteColorPercent
#     , namesUnderSpaceObjectIcon = namesUnderSpaceObjectIcon
#     , bgColorFillsPercent = bgColorFillsPercent
#     , rightAlignedIconsHints = rightAlignedIconsHints
#     , commonIndications = commonIndications
#     }


def parseOverviewEntryDistanceInMetersFromText(distanceDisplayTextBeforeTrim: str) -> Union[str, int]:
    print("[base parseOverviewEntryDistanceInMetersFromText] Starting Function.")
    try:
        reversedNumberTexts = distanceDisplayTextBeforeTrim.strip().split(" ")[-1]
        unitInMeters = parseDistanceUnitInMeters(reversedNumberTexts)
        print(reversedNumberTexts)
        if unitInMeters is None: raise Exception(f"Failed to Parse Distance Unit Text of '{reversedNumberTexts}'")
        
        parsedNumber = parseNumberTruncatingAfterOptionalDecimalSeparator(reversedNumberTexts)
        print("ParsedNumber: ", parsedNumber, type(parsedNumber))
        return parsedNumber * unitInMeters
    except Exception as e:
        print("Exception caught Parsing Overview. ", e)
# parseOverviewEntryDistanceInMetersFromText : str -> Result str int
# parseOverviewEntryDistanceInMetersFromText distanceDisplayTextBeforeTrim =
#     case distanceDisplayTextBeforeTrim |> str.trim |> str.split " " |> List.reverse of
#          :: reversedNumberTexts ->
#             case parseDistanceUnitInMeters unitText of
#                 Nothing ->
#                     Err ("Failed to parse distance unit text of '" ++ unitText ++ "'")
#                 Just unitInMeters ->
#                     case
#                         reversedNumberTexts |> List.reverse |> str.join " " |> parseNumberTruncatingAfterOptionalDecimalSeparator
#                     of
#                         Err parseNumberError ->
#                             Err ("Failed to parse number: " ++ parseNumberError)
#                         Ok parsedNumber ->
#                             Ok (parsedNumber * unitInMeters)
#         _ ->
#             Err "Expecting at least one whitespace character separating number and unit."


def parseDistanceUnitInMeters(unitText: str) -> Optional[int]:
    if unitText == 'm': return 1
    if unitText == 'km': return 1000
    return None
# parseDistanceUnitInMeters : str -> Maybe int
# parseDistanceUnitInMeters unitText =
#     case str.trim unitText of
#         "m" ->
#             Just 1
#         "km" ->
#             Just 1000
#         _ ->
#             Nothing


def parseSelectedItemWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[SelectedItemWindow]:
    data = [parseSelectedItemWindow(x) for x in listDescendantsWithDisplayRegion(uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'ActiveItem']
    return None if len(data) == 0 else data[0]
# parseSelectedItemWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SelectedItemWindow
# parseSelectedItemWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ActiveItem")
#         |> List.head
#         |> Maybe.map parseSelectedItemWindow


def parseSelectedItemWindow(windowNode: UITreeNodeWithDisplayRegion) -> SelectedItemWindow:
    raise NotImplementedError()
# parseSelectedItemWindow : UITreeNodeWithDisplayRegion -> SelectedItemWindow
# parseSelectedItemWindow windowNode =
#     let
#         actionButtonFromTexturePathEnding texturePathEnding =
#             windowNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (.uiNode
#                         >> getTexturePathFromDictEntries
#                         >> Maybe.map (str.toLower >> str.endsWith (str.toLower texturePathEnding))
#                         >> Maybe.withDefault False
#                     )
#                 |> List.head
#         orbitButton =
#             actionButtonFromTexturePathEnding "44_32_21.png"
#     in
#     { uiNode = windowNode, orbitButton = orbitButton }


def parseDronesWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[DronesWindow]:
    _droneViews = [x for x in listDescendantsWithDisplayRegion(
        uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'DroneView']
    if len(_droneViews) == 0:
        return None
    _droneView = _droneViews[0]
    scrollNodes = []
    droneEntries = []
    droneGroupHeaders = []
    for x in listChildrenWithDisplayRegion(_droneView):
        if 'scroll' in x.uiNode.pythonObjectTypeName.lower():
            scrollNodes.append(x)
        if x.uiNode.pythonObjectTypeName == 'Group':
            droneGroupHeaders.append(x)
        if x.uiNode.pythonObjectTypeName == 'DroneEntry':
            droneEntries.append(x)
    droneGroups = [DronesWindowEntryDrone(**x) for x in droneEntries]
    droneGroups.extend([DronesWindowEntryGroup(
        header=x, children=[]) for x in droneGroups])
    droneGroups = dronesGroupTreesFromFlatListOfEntries(droneGroups)

    def droneGroupFromHeaderTextPart(headerTextPart: str) -> Optional[DronesWindowEntryGroupStructure]:
        _data = [x for x in droneGroups if headerTextPart.lower()
                 in x.header.maintext.lower()]
        sorted(_data, key=len)
        return _data[0] if len(_data) > 0 else None
    droneWindow = DronesWindow()
    droneWindow.uiNode = _droneView
    droneWindow.droneGroupInBay = droneGroups
    droneWindow.droneGroupInLocalSpace = droneGroupFromHeaderTextPart("in Bay")
    droneWindow.droneGroups = droneGroupFromHeaderTextPart("in local space")
    return droneWindow


# parseDronesWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe DronesWindow
# parseDronesWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DroneView")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 {-
#                    scrollNode =
#                        windowNode
#                            |> listDescendantsWithDisplayRegion
#                            |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                            |> List.head
#                 -}
#                 droneGroupHeaders =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Group")
#                         |> List.filterMap parseDronesWindowDroneGroupHeader
#                 droneEntries =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DroneEntry")
#                         |> List.map parseDronesWindowDroneEntry
#                 droneGroups =
#                     [ droneEntries |> List.map DronesWindowEntryDrone
#                     , droneGroupHeaders
#                         |> List.map (\header -> { header = header, children = [] })
#                         |> List.map DronesWindowEntryGroup
#                     ]
#                         |> List.concat
#                         |> dronesGroupTreesFromFlatListOfEntries
#                 droneGroupFromHeaderTextPart headerTextPart =
#                     droneGroups
#                         |> List.filter (.header >> .maintext >> Maybe.withDefault "" >> str.toLower >> str.contains (headerTextPart |> str.toLower))
#                         |> List.sortBy (.header >> .maintext >> Maybe.map str.length >> Maybe.withDefault 999)
#                         |> List.head
#             in
#             Just
#                 { uiNode = windowNode
#                 , droneGroups = droneGroups
#                 , droneGroupInBay = droneGroupFromHeaderTextPart "in Bay"
#                 , droneGroupInLocalSpace = droneGroupFromHeaderTextPart "in local space"
#                 }


def dronesGroupTreesFromFlatListOfEntries(entriesBeforeOrdering: List[Union[DronesWindowEntryGroup, DronesWindowEntryDrone]]) -> List[DronesWindowEntryGroupStructure]:
    def verticalOffsetFromEntry(entry: Union[DronesWindowEntryGroup, DronesWindowEntryDrone]):
        if type(entry) == DronesWindowEntryDrone:
            return entry.uiNode.totalDisplayRegion.y
        if type(entry) == DronesWindowEntryGroup:
            return entry.header.uiNode.totalDisplayRegion.y
        raise Exception("Entry type Incorrect")
    entriesOrderedVertically = sorted(
        entriesBeforeOrdering, key=verticalOffsetFromEntry)
    result: List[DronesWindowEntryGroup] = []
    for x in entriesOrderedVertically:
        if type(x) == DronesWindowEntryDrone:
            raise NotImplementedError()
        if type(x) == DronesWindowEntryGroup:
            result.append(x)
    if len(result) > 0:
        topmostGroupEntry = result[0]
        _topEntry = verticalOffsetFromEntry(topmostGroupEntry)
        entriesUpToSibling = [
            x for x in entriesOrderedVertically if verticalOffsetFromEntry(x) <= _topEntry]
        entriesUpToSibling = [x for x in entriesUpToSibling if type(
            x) is DronesWindowEntryDrone]
        childGroupTrees = dronesGroupTreesFromFlatListOfEntries(
            entriesUpToSibling)
        childDrones = [x for x in entriesUpToSibling if type(
            x) == DronesWindowEntryDrone]
        children = childDrones
        children.extend([DronesWindowEntryGroup(**x) for x in childGroupTrees])
        children.sort(verticalOffsetFromEntry)
        topmostGroupTree = DronesWindowEntryGroupStructure(**{
            "header": topmostGroupEntry.header,
            "children": children
        })
        bottommostDescendantOffset = enumerateDescendantsOfDronesGroup(
            topmostGroupTree)
        defaultVal = verticalOffsetFromEntry(topmostGroupTree)
        bottommostDescendantOffset = max([verticalOffsetFromEntry(
            x) for x in bottommostDescendantOffset]) if len(bottommostDescendantOffset) > 0 else defaultVal
        entriesBelow = [x for x in entriesOrderedVertically if verticalOffsetFromEntry(
            x) <= bottommostDescendantOffset]
        return [topmostGroupTree].extend(dronesGroupTreesFromFlatListOfEntries(entriesBelow))
    return []

# dronesGroupTreesFromFlatListOfEntries : List DronesWindowEntry -> List DronesWindowEntryGroupStructure
# dronesGroupTreesFromFlatListOfEntries entriesBeforeOrdering =
#     let
#         verticalOffsetFromEntry entry =
#             case entry of
#                 DronesWindowEntryDrone droneEntry ->
#                     droneEntry.uiNode.totalDisplayRegion.y
#                 DronesWindowEntryGroup groupEntry ->
#                     groupEntry.header.uiNode.totalDisplayRegion.y
#         entriesOrderedVertically =
#             entriesBeforeOrdering
#                 |> List.sortBy verticalOffsetFromEntry
#     in
#     entriesOrderedVertically
#         |> List.filterMap
#             (\entry ->
#                 case entry of
#                     DronesWindowEntryDrone _ ->
#                         Nothing
#                     DronesWindowEntryGroup group ->
#                         Just group
#             )
#         |> List.head
#         |> Maybe.map
#             (\topmostGroupEntry ->
#                 let
#                     entriesUpToSibling =
#                         entriesOrderedVertically
#                             |> List.Extra.dropWhile
#                                 (verticalOffsetFromEntry
#                                     >> (\offset -> offset <= verticalOffsetFromEntry (DronesWindowEntryGroup topmostGroupEntry))
#                                 )
#                             |> List.Extra.takeWhile
#                                 (\entry ->
#                                     case entry of
#                                         DronesWindowEntryDrone _ ->
#                                             True
#                                         DronesWindowEntryGroup group ->
#                                             topmostGroupEntry.header.expander.uiNode.totalDisplayRegion.x
#                                                 < (group.header.expander.uiNode.totalDisplayRegion.x - 3)
#                                 )
#                     childGroupTrees =
#                         dronesGroupTreesFromFlatListOfEntries entriesUpToSibling
#                     childDrones =
#                         entriesUpToSibling
#                             |> List.Extra.takeWhile
#                                 (\entry ->
#                                     case entry of
#                                         DronesWindowEntryDrone _ ->
#                                             True
#                                         DronesWindowEntryGroup _ ->
#                                             False
#                                 )
#                     children =
#                         [ childDrones, childGroupTrees |> List.map DronesWindowEntryGroup ]
#                             |> List.concat
#                             |> List.sortBy verticalOffsetFromEntry
#                     topmostGroupTree =
#                         { header = topmostGroupEntry.header
#                         , children = children
#                         }
#                     bottommostDescendantOffset =
#                         enumerateDescendantsOfDronesGroup topmostGroupTree
#                             |> List.map verticalOffsetFromEntry
#                             |> List.maximum
#                             |> Maybe.withDefault (verticalOffsetFromEntry (DronesWindowEntryGroup topmostGroupTree))
#                     entriesBelow =
#                         entriesOrderedVertically
#                             |> List.Extra.dropWhile (verticalOffsetFromEntry >> (\offset -> offset <= bottommostDescendantOffset))
#                 in
#                 topmostGroupTree :: dronesGroupTreesFromFlatListOfEntries entriesBelow
#             )
#         |> Maybe.withDefault []


def enumerateAllDronesFromDronesGroup(x: DronesWindowEntryGroupStructure) -> List[DronesWindowEntryDroneStructure]:
    return [y for y in enumerateDescendantsOfDronesGroup(x) if type(y) == DronesWindowEntryDrone]
# enumerateAllDronesFromDronesGroup : DronesWindowEntryGroupStructure -> List DronesWindowEntryDroneStructure
# enumerateAllDronesFromDronesGroup =
#     enumerateDescendantsOfDronesGroup
#         >> List.filterMap
#             (\entry ->
#                 case entry of
#                     DronesWindowEntryDrone drone ->
#                         Just drone
#                     DronesWindowEntryGroup _ ->
#                         Nothing
#             )


def enumerateDescendantsOfDronesGroup(group: DronesWindowEntryGroupStructure) -> List[Union[DronesWindowEntryGroup, DronesWindowEntryDrone]]:
    result = []
    for x in group.children:
        if type(x) == DronesWindowEntryDrone:
            result = [x]
        if type(x) == DronesWindowEntryGroup:
            result = [x].extend(enumerateAllDronesFromDronesGroup(x))
    return result
# enumerateDescendantsOfDronesGroup : DronesWindowEntryGroupStructure -> List DronesWindowEntry
# enumerateDescendantsOfDronesGroup group =
#     group.children
#         |> List.concatMap
#             (\child ->
#                 case child of
#                     DronesWindowEntryDrone _ ->
#                         [ child ]
#                     DronesWindowEntryGroup childGroup ->
#                         child :: enumerateDescendantsOfDronesGroup childGroup
#             )


def parseDronesWindowDroneGroupHeader(groupHeaderUiNode: UITreeNodeWithDisplayRegion) -> Optional[DronesWindowDroneGroupHeader]:
    expander = [x for x in listDescendantsWithDisplayRegion(
        groupHeaderUiNode) for y in getNameFromDictEntries(x.uiNode) if "expander" in y.lower()]
    if len(expander) == 0:
        return None
    maintext = getAllContainedDisplayTextsWithRegion(groupHeaderUiNode)
    maintext.sort(key=lambda x: areaFromDisplayRegion(x[1].totalDisplayRegion))
    maintext = [x[0] for x in maintext]
    maintext = maintext[0] if len(maintext) > 0 else None
    quantityFromTitle = parseQuantityFromDroneGroupTitleText(maintext)
    result = DronesWindowDroneGroupHeader()
    result.maintext = maintext
    result.expander = parseExpander(expander[0])
    result.quantityFromTitle = quantityFromTitle
    result.uiNode = groupHeaderUiNode
    return result


# parseDronesWindowDroneGroupHeader : UITreeNodeWithDisplayRegion -> Maybe DronesWindowDroneGroupHeader
# parseDronesWindowDroneGroupHeader groupHeaderUiNode =
#     case
#         groupHeaderUiNode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter
#                 (.uiNode
#                     >> getNameFromDictEntries
#                     >> (Maybe.map (str.toLower >> str.contains "expander") >> Maybe.withDefault False)
#                 )
#     of
#         [ expanderNode ] ->
#             let
#                 maintext =
#                     groupHeaderUiNode
#                         |> getAllContainedDisplayTextsWithRegion
#                         |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                         |> List.map Tuple.first
#                         |> List.head
#                 quantityFromTitle =
#                     maintext |> Maybe.andThen (parseQuantityFromDroneGroupTitleText >> Result.withDefault Nothing)
#             in
#             Just
#                 { uiNode = groupHeaderUiNode
#                 , maintext = maintext
#                 , expander = expanderNode |> parseExpander
#                 , quantityFromTitle = quantityFromTitle
#                 }
#         _ ->
#             Nothing


def parseQuantityFromDroneGroupTitleText(droneGroupTitleText: str) -> Optional[Union[str, int]]:
    textAfterOpeningParenthesis = droneGroupTitleText.split("(")[1:]
    if len(textAfterOpeningParenthesis) == 0:
        return None
    _list = "".join(textAfterOpeningParenthesis).split(")")
    try:
        if len(_list) == 0:
            return None
        try:
            s = _list[0].strip()
            data = int(s)
            return data
        except:
            return f"Failed to parse to integer from '{s}'"
    except:
        return "Found unexpected number of parentheses."

# parseQuantityFromDroneGroupTitleText : str -> Result str (Maybe int)
# parseQuantityFromDroneGroupTitleText droneGroupTitleText =
#     case droneGroupTitleText |> str.split "(" |> List.drop 1 of
#         [] ->
#             Ok Nothing
#         [ textAfterOpeningParenthesis ] ->
#             textAfterOpeningParenthesis
#                 |> str.split ")"
#                 |> List.head
#                 |> Maybe.andThen (str.trim >> str.toint)
#                 |> Result.fromMaybe ("Failed to parse to integer from '" ++ textAfterOpeningParenthesis ++ "'")
#                 |> Result.map Just
#         _ ->
#             Err "Found unexpected number of parentheses."


def parseDronesWindowDroneEntry(droneEntryNode: UITreeNodeWithDisplayRegion) -> DronesWindowEntryDroneStructure:
    maintext = getAllContainedDisplayTextsWithRegion(droneEntryNode)
    maintext.sort(key=lambda x: areaFromDisplayRegion(
        x[1].totalDisplayRegion) or 0)
    maintext = [x[0] for x in maintext][0]

    def gaugeValuePercentFromContainerName(containerName: str):
        gaugeNode = [x for x in listDescendantsWithDisplayRegion(
            droneEntryNode) if getNameFromDictEntries(x.uiNode) == containerName][0]

        def gaudeDescendantFromName(gaugeDescendantName: str) -> List[UITreeNodeWithDisplayRegion]:
            return [x for x in listDescendantsWithDisplayRegion(gaugeNode) if getNameFromDictEntries(x.uiNode) == gaugeDescendantName]

        gaugeBar = gaudeDescendantFromName("droneGaugeBar")
        droneGaugeBarDmg = gaudeDescendantFromName("droneGaugeBarDmg")
        return ((gaugeBar.totalDisplayRegion.width - droneGaugeBarDmg.totalDisplayRegion.width) * 100) // gaugeBar.totalDisplayRegion.width

    shieldPercent = gaugeValuePercentFromContainerName("gauge_shield")
    armorPercent = gaugeValuePercentFromContainerName("gauge_armor")
    structPercent = gaugeValuePercentFromContainerName("gauge_struct")

    result = DronesWindowEntryDroneStructure()
    result.hitpointsPercent = Hitpoints(
        armor=armorPercent, shield=shieldPercent, structure=structPercent)
    result.maintext = maintext
    result.uiNode = droneEntryNode
    return result


# parseDronesWindowDroneEntry : UITreeNodeWithDisplayRegion -> DronesWindowEntryDroneStructure
# parseDronesWindowDroneEntry droneEntryNode =
#     let
#         maintext =
#             droneEntryNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.map Tuple.first
#                 |> List.head
#         gaugeValuePercentFromContainerName containerName =
#             droneEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just containerName))
#                 |> List.head
#                 |> Maybe.andThen
#                     (\gaugeNode ->
#                         let
#                             gaudeDescendantFromName gaugeDescendantName =
#                                 gaugeNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just gaugeDescendantName))
#                                     |> List.head
#                         in
#                         gaudeDescendantFromName "droneGaugeBar"
#                             |> Maybe.andThen
#                                 (\gaugeBar ->
#                                     gaudeDescendantFromName "droneGaugeBarDmg"
#                                         |> Maybe.map
#                                             (\droneGaugeBarDmg ->
#                                                 ((gaugeBar.totalDisplayRegion.width - droneGaugeBarDmg.totalDisplayRegion.width) * 100)
#                                                     // gaugeBar.totalDisplayRegion.width
#                                             )
#                                 )
#                     )
#         hitpointsPercent =
#             gaugeValuePercentFromContainerName "gauge_shield"
#                 |> Maybe.andThen
#                     (\shieldPercent ->
#                         gaugeValuePercentFromContainerName "gauge_armor"
#                             |> Maybe.andThen
#                                 (\armorPercent ->
#                                     gaugeValuePercentFromContainerName "gauge_struct"
#                                         |> Maybe.map
#                                             (\structPercent ->
#                                                 { shield = shieldPercent
#                                                 , armor = armorPercent
#                                                 , structure = structPercent
#                                                 }
#                                             )
#                                 )
#                     )
#     in
#     { uiNode = droneEntryNode
#     , maintext = maintext
#     , hitpointsPercent = hitpointsPercent
#     }


def parseProbeScannerWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ProbeScannerWindow]:
    displayRegion = [x for x in listDescendantsWithDisplayRegion(
        uiTreeRoot) if x.uiNode.pythonObjectTypeName == "ProbeScannerWindow"]
    if len(displayRegion) == 0:
        return None
    windowNode = displayRegion[0]
    scanResultsNodes: List[UITreeNodeWithDisplayRegion] = []
    scrollnodes: List[UITreeNodeWithDisplayRegion] = []
    for x in listDescendantsWithDisplayRegion(windowNode):
        if x.uiNode.pythonObjectTypeName == "ScanResultNew":
            scanResultsNodes.append(x)
        if "ResultsContainer" in getNameFromDictEntries(x.uiNode):
            scrollnodes.extend([y for y in listDescendantsWithDisplayRegion(
                x) if 'scroll' in y.uiNode.pythonObjectTypeName.lower()])
    scrollnode = scrollnodes[0]
    headersContainerNode = [x for x in listDescendantsWithDisplayRegion(
        scrollnode) if 'header' in x.uiNode.pythonObjectTypeName.lower()][0]
    entriesHeaders = getAllContainedDisplayTextsWithRegion(
        headersContainerNode)
    scanResults = [parseProbeScanResult(
        entriesHeaders, x) for x in scanResultsNodes]

    result = ProbeScannerWindow()
    result.uiNode = windowNode
    result.scanResults = scanResults
    return result

# parseProbeScannerWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ProbeScannerWindow
# parseProbeScannerWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ProbeScannerWindow")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 scanResultsNodes =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ScanResultNew")
#                 scrollNode =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.contains "ResultsContainer") >> Maybe.withDefault False)
#                         |> List.concatMap listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.head
#                 headersContainerNode =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "header")
#                         |> List.head
#                 entriesHeaders =
#                     headersContainerNode
#                         |> Maybe.map getAllContainedDisplayTextsWithRegion
#                         |> Maybe.withDefault []
#                 scanResults =
#                     scanResultsNodes
#                         |> List.map (parseProbeScanResult entriesHeaders)
#             in
#             Just { uiNode = windowNode, scanResults = scanResults }


def parseProbeScanResult(entriesHeaders: List[Tuple[str, UITreeNodeWithDisplayRegion]], scanResultNode: UITreeNodeWithDisplayRegion) -> ProbeScanResult:
    textsLeftToRight = getAllContainedDisplayTextsWithRegion(scanResultNode)
    textsLeftToRight.sort(key=lambda x: x[1].totalDisplayRegion.x)
    textsLeftToRight = [x[0] for x in textsLeftToRight]
    maybeHeader = []
    for cellText, cell in getAllContainedDisplayTextsWithRegion(scanResultNode):
        cellMiddle = cell.totalDisplayRegion.x + \
            (cell.totalDisplayRegion.width // 2)
        header = [header for _, header in entriesHeaders if header.totalDisplayRegion.x < (
            cellMiddle + 1) and cellMiddle < (header.totalDisplayRegion.x+header.totalDisplayRegion.width - 1)][0]
        maybeHeader.append((header, cellText))
    warpButton = [x for x in listDescendantsWithDisplayRegion(scanResultNode) if (
        getTexturePathFromDictEntries(x.uiNode) or '').endswith('44_32_18.png')][0]
    result = ProbeScanResult()
    result.warpButton = warpButton
    result.textsLeftToRight = textsLeftToRight
    result.uiNode = scanResultNode
    result.cellsTexts = {k: v for k, v in maybeHeader}
    return result

# parseProbeScanResult : List ( str, UITreeNodeWithDisplayRegion ) -> UITreeNodeWithDisplayRegion -> ProbeScanResult
# parseProbeScanResult entriesHeaders scanResultNode =
#     let
#         textsLeftToRight =
#             scanResultNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .x)
#                 |> List.map Tuple.first
#         cellsTexts =
#             scanResultNode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.filterMap
#                     (\( cellText, cell ) ->
#                         let
#                             cellMiddle =
#                                 cell.totalDisplayRegion.x + (cell.totalDisplayRegion.width // 2)
#                             maybeHeader =
#                                 entriesHeaders
#                                     |> List.filter
#                                         (\( _, header ) ->
#                                             header.totalDisplayRegion.x
#                                                 < cellMiddle
#                                                 + 1
#                                                 && cellMiddle
#                                                 < header.totalDisplayRegion.x
#                                                 + header.totalDisplayRegion.width
#                                                 - 1
#                                         )
#                                     |> List.head
#                         in
#                         maybeHeader
#                             |> Maybe.map (\( headerText, _ ) -> ( headerText, cellText ))
#                     )
#                 |> Dict.fromList
#         warpButton =
#             scanResultNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getTexturePathFromDictEntries >> Maybe.map (str.endsWith "44_32_18.png") >> Maybe.withDefault False)
#                 |> List.head
#     in
#     { uiNode = scanResultNode
#     , textsLeftToRight = textsLeftToRight
#     , cellsTexts = cellsTexts
#     , warpButton = warpButton
#     }


def parseDirectionalScannerWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[DirectionalScannerWindow]:
    displayRegions = [x for x in listDescendantsWithDisplayRegion(
        uiTreeRoot) if x.uiNode.pythonObjectTypeName == "DirectionalScanner"]
    if len(displayRegions) == 0:
        return None
    windowNode = displayRegions[0]
    scrollNode = [x for x in listDescendantsWithDisplayRegion(
        windowNode) if 'scroll' in x.uiNode.pythonObjectTypeName.lower()]
    scrollNode.sort(key=lambda x: areaFromDisplayRegion(
        x.totalDisplayRegion) or 0)  # Possibly need to Reverse?
    scrollNode = scrollNode[0]

    scanResultsNodes = [x for x in listDescendantsWithDisplayRegion(
        scrollNode) if x.uiNode.pythonObjectTypeName == 'DirectionalScanResultEntry']
    result = DirectionalScannerWindow()
    result.scanResults = scanResultsNodes
    result.scrollNode = scrollNode
    result.uiNode = windowNode
    return result

# parseDirectionalScannerWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe DirectionalScannerWindow
# parseDirectionalScannerWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DirectionalScanner")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 scrollNode =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> str.toLower >> str.contains "scroll")
#                         |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0 >> negate)
#                         |> List.head
#                 scanResultsNodes =
#                     scrollNode
#                         |> Maybe.map listDescendantsWithDisplayRegion
#                         |> Maybe.withDefault []
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "DirectionalScanResultEntry")
#             in
#             Just
#                 { uiNode = windowNode
#                 , scrollNode = scrollNode
#                 , scanResults = scanResultsNodes
#                 }


def parseStationWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[StationWindow]:
    displayRegions = [x for x in listDescendantsWithDisplayRegion(
        uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'LobbyWnd']
    if len(displayRegions) == 0:
        return None
    windowNode = displayRegions[0]
    buttons = [x for x in listDescendantsWithDisplayRegion(
        windowNode) if x.uiNode.pythonObjectTypeName == 'Button']

    def buttonFromDisplayText(textToSearch: str):
        textToSearchLowercase = textToSearch.lower()

        def textMatches(text):
            return text == textToSearchLowercase or (f">{textToSearchLowercase}<") in text
        _r = [y for x in buttons for y in getAllContainedDisplayTexts(
            x.uiNode) if textMatches(y.lower().strip())]
        return _r[0] if len(_r) > 0 else None
    result = StationWindow()
    result.uiNode = windowNode
    result.undockButton = buttonFromDisplayText("undock")
    result.abortUndockButton = buttonFromDisplayText("undocking")
    return result
# parseStationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe StationWindow
# parseStationWindowFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "LobbyWnd")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just windowNode ->
#             let
#                 buttons =
#                     windowNode
#                         |> listDescendantsWithDisplayRegion
#                         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Button")
#                 buttonFromDisplayText textToSearch =
#                     let
#                         textToSearchLowercase =
#                             str.toLower textToSearch
#                         textMatches text =
#                             text == textToSearchLowercase || (text |> str.contains (">" ++ textToSearchLowercase ++ "<"))
#                     in
#                     buttons
#                         |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.toLower >> str.trim) >> List.any textMatches)
#                         |> List.head
#             in
#             Just
#                 { uiNode = windowNode
#                 , undockButton = buttonFromDisplayText "undock"
#                 , abortUndockButton = buttonFromDisplayText "undocking"
#                 }


def parseInventoryWindowsFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[InventoryWindow]:
    return [parseInventoryWindow(x) for x in listDescendantsWithDisplayRegion(uiTreeRoot) if "InventoryPrimary" in x.uiNode.pythonObjectTypeName or 'ActiveShipCargo' in x.uiNode.pythonObjectTypeName]
# parseInventoryWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List InventoryWindow
# parseInventoryWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (\uiNode -> [ "InventoryPrimary", "ActiveShipCargo" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#         |> List.map parseInventoryWindow


def parseInventoryWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> InventoryWindow:
    raise NotImplementedError()
# parseInventoryWindow : UITreeNodeWithDisplayRegion -> InventoryWindow
# parseInventoryWindow windowUiNode =
#     let
#         selectedContainerCapacityGaugeNode =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "CapacityGauge")
#                 |> List.head
#         selectedContainerCapacityGauge =
#             selectedContainerCapacityGaugeNode
#                 |> Maybe.map (.uiNode >> listDescendantsInUITreeNode)
#                 |> Maybe.withDefault []
#                 |> List.filterMap getDisplayText
#                 |> List.sortBy (str.length >> negate)
#                 |> List.head
#                 |> Maybe.map parseInventoryCapacityGaugeText
#         leftTreeEntriesRootNodes =
#             windowUiNode |> getContainedTreeViewEntryRootNodes
#         leftTreeEntries =
#             leftTreeEntriesRootNodes |> List.map parseInventoryWindowTreeViewEntry
#         rightContainerNode =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (\uiNode ->
#                         (uiNode.uiNode.pythonObjectTypeName == "Container")
#                             && (uiNode.uiNode |> getNameFromDictEntries |> Maybe.map (str.contains "right") |> Maybe.withDefault False)
#                     )
#                 |> List.head
#         subCaptionLabelText =
#             rightContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.startsWith "subCaptionLabel") >> Maybe.withDefault False)
#                 |> List.concatMap (.uiNode >> getAllContainedDisplayTexts)
#                 |> List.head
#         maybeSelectedContainerInventoryNode =
#             rightContainerNode
#                 |> Maybe.andThen
#                     (listDescendantsWithDisplayRegion
#                         >> List.filter
#                             (\uiNode ->
#                                 [ "ShipCargo", "ShipDroneBay", "ShipGeneralMiningHold", "StationItems", "ShipFleetHangar", "StructureItemHangar" ]
#                                     |> List.member uiNode.uiNode.pythonObjectTypeName
#                             )
#                         >> List.head
#                     )
#         selectedContainerInventory =
#             maybeSelectedContainerInventoryNode
#                 |> Maybe.map
#                     (\selectedContainerInventoryNode ->
#                         let
#                             listViewItemNodes =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Item")
#                             scrollControlsNode =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                                     |> List.head
#                             notListViewItemNodes =
#                                 selectedContainerInventoryNode
#                                     |> listDescendantsWithDisplayRegion
#                                     |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "InvItem")
#                             itemsView =
#                                 if 0 < (listViewItemNodes |> List.length) then
#                                     Just (InventoryItemsListView { items = listViewItemNodes })
#                                 else if 0 < (notListViewItemNodes |> List.length) then
#                                     Just (InventoryItemsNotListView { items = notListViewItemNodes })
#                                 else
#                                     Nothing
#                         in
#                         { uiNode = selectedContainerInventoryNode
#                         , itemsView = itemsView
#                         , scrollControls = scrollControlsNode |> Maybe.map parseScrollControls
#                         }
#                     )
#         buttonToSwitchToListView =
#             rightContainerNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter
#                     (\uiNode ->
#                         (uiNode.uiNode.pythonObjectTypeName |> str.contains "ButtonIcon")
#                             && ((uiNode.uiNode |> getTexturePathFromDictEntries |> Maybe.withDefault "") |> str.endsWith "38_16_190.png")
#                     )
#                 |> List.head
#     in
#     { uiNode = windowUiNode
#     , leftTreeEntries = leftTreeEntries
#     , subCaptionLabelText = subCaptionLabelText
#     , selectedContainerCapacityGauge = selectedContainerCapacityGauge
#     , selectedContainerInventory = selectedContainerInventory
#     , buttonToSwitchToListView = buttonToSwitchToListView
#     }


def getContainedTreeViewEntryRootNodes(parentNode: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    leftTreeEntriesAllNodes = [x for x in listDescendantsWithDisplayRegion(
        parentNode) if x.uiNode.pythonObjectTypeName.startswith("TreeViewEntry")]

    def isContainedintreeEntry(candidate):
        result = []
        for x in leftTreeEntriesAllNodes:
            result.extend(listDescendantsWithDisplayRegion(x))
        return candidate in result
    return [x for x in leftTreeEntriesAllNodes if not isContainedintreeEntry(x)]

# getContainedTreeViewEntryRootNodes : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# getContainedTreeViewEntryRootNodes parentNode =
#     let
#         leftTreeEntriesAllNodes =
#             parentNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.startsWith "TreeViewEntry")
#         isContainedintreeEntry candidate =
#             leftTreeEntriesAllNodes
#                 |> List.concatMap listDescendantsWithDisplayRegion
#                 |> List.member candidate
#     in
#     leftTreeEntriesAllNodes
#         |> List.filter (isContainedintreeEntry >> not)


def parseInventoryWindowTreeViewEntry(treeEntryNode: UITreeNodeWithDisplayRegion) -> InventoryWindowLeftTreeEntry:
    raise NotImplementedError()
# parseInventoryWindowTreeViewEntry : UITreeNodeWithDisplayRegion -> InventoryWindowLeftTreeEntry
# parseInventoryWindowTreeViewEntry treeEntryNode =
#     let
#         topContNode =
#             treeEntryNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.startsWith "topCont_") >> Maybe.withDefault False)
#                 |> List.sortBy (.totalDisplayRegion >> .y)
#                 |> List.head
#         toggleBtn =
#             topContNode
#                 |> Maybe.map listDescendantsWithDisplayRegion
#                 |> Maybe.withDefault []
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map ((==) "toggleBtn") >> Maybe.withDefault False)
#                 |> List.head
#         text =
#             topContNode
#                 |> Maybe.map getAllContainedDisplayTextsWithRegion
#                 |> Maybe.withDefault []
#                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> .y)
#                 |> List.head
#                 |> Maybe.map Tuple.first
#                 |> Maybe.withDefault ""
#         childrenNodes =
#             treeEntryNode |> getContainedTreeViewEntryRootNodes
#         children =
#             childrenNodes |> List.map (parseInventoryWindowTreeViewEntry >> InventoryWindowLeftTreeEntryChild)
#     in
#     { uiNode = treeEntryNode
#     , toggleBtn = toggleBtn
#     , selectRegion = topContNode
#     , text = text
#     , children = children
#     }


def unwrapInventoryWindowLeftTreeEntryChild(child: InventoryWindowLeftTreeEntryChild) -> InventoryWindowLeftTreeEntry:
    if type(child) == InventoryWindowLeftTreeEntryChild:
        return child
# unwrapInventoryWindowLeftTreeEntryChild : InventoryWindowLeftTreeEntryChild -> InventoryWindowLeftTreeEntry
# unwrapInventoryWindowLeftTreeEntryChild child =
#     case child of
#         InventoryWindowLeftTreeEntryChild unpacked ->
#             unpacked


def parseInventoryCapacityGaugeText(capacityText: str) -> Union[str, InventoryWindowCapacityGauge]:
    raise NotImplementedError()
# parseInventoryCapacityGaugeText : str -> Result str InventoryWindowCapacityGauge
# parseInventoryCapacityGaugeText capacityText =
#     let
#         parseMaybeNumber =
#             Maybe.map (str.trim >> parseNumberTruncatingAfterOptionalDecimalSeparator >> Result.map Just)
#                 >> Maybe.withDefault (Ok Nothing)
#         continueWithTexts { usedText, maybeMaximumText, maybeSelectedText } =
#             case usedText |> parseNumberTruncatingAfterOptionalDecimalSeparator of
#                 Err parseNumberError ->
#                     Err ("Failed to parse used number: " ++ parseNumberError)
#                 Ok used ->
#                     case maybeMaximumText |> parseMaybeNumber of
#                         Err parseNumberError ->
#                             Err ("Failed to parse maximum number: " ++ parseNumberError)
#                         Ok maximum ->
#                             case maybeSelectedText |> parseMaybeNumber of
#                                 Err parseNumberError ->
#                                     Err ("Failed to parse selected number: " ++ parseNumberError)
#                                 Ok selected ->
#                                     Ok { used = used, maximum = maximum, selected = selected }
#         continueAfterSeparatingBySlash { beforeSlashText, afterSlashMaybeText } =
#             case beforeSlashText |> str.trim |> str.split ")" of
#                 [ onlyUsedText ] ->
#                     continueWithTexts { usedText = onlyUsedText, maybeMaximumText = afterSlashMaybeText, maybeSelectedText = Nothing }
#                 [ firstPart, secondPart ] ->
#                     continueWithTexts { usedText = secondPart, maybeMaximumText = afterSlashMaybeText, maybeSelectedText = Just (firstPart |> str.replace "(" "") }
#                 _ ->
#                     Err ("Unexpected number of components in text before slash '" ++ beforeSlashText ++ "'")
#     in
#     case capacityText |> str.replace "m??" "" |> str.split "/" of
#         [ withoutSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = withoutSlash, afterSlashMaybeText = Nothing }
#         [ partBeforeSlash, partAfterSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = partBeforeSlash, afterSlashMaybeText = Just partAfterSlash }
#         _ ->
#             Err ("Unexpected number of components in capacityText '" ++ capacityText ++ "'")


def parseModuleButtonTooltipFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[ModuleButtonTooltip]:
     data = [x for x in listDescendantsWithDisplayRegion(uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'ModuleButtonTooltip']
     if len(data) == 0: return None
     return parseModuleButtonTooltip(data[0])
# parseModuleButtonTooltipFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe ModuleButtonTooltip
# parseModuleButtonTooltipFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ModuleButtonTooltip")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just uiNode ->
#             Just (parseModuleButtonTooltip uiNode)


def parseModuleButtonTooltip(tooltipUINode: UITreeNodeWithDisplayRegion) -> ModuleButtonTooltip:
    raise NotImplementedError()
# parseModuleButtonTooltip : UITreeNodeWithDisplayRegion -> ModuleButtonTooltip
# parseModuleButtonTooltip tooltipUINode =
#     let
#         upperRightCornerFromDisplayRegion region =
#             { x = region.x + region.width, y = region.y }
#         distanceSquared a b =
#             let
#                 distanceX =
#                     a.x - b.x
#                 distanceY =
#                     a.y - b.y
#             in
#             distanceX * distanceX + distanceY * distanceY
#         shortcutCandidates =
#             tooltipUINode
#                 |> getAllContainedDisplayTextsWithRegion
#                 |> List.map
#                     (\( text, textUINode ) ->
#                         { text = text
#                         , distanceUpperRightCornerSquared =
#                             distanceSquared
#                                 (textUINode.totalDisplayRegion |> upperRightCornerFromDisplayRegion)
#                                 (tooltipUINode.totalDisplayRegion |> upperRightCornerFromDisplayRegion)
#                         }
#                     )
#                 |> List.sortBy .distanceUpperRightCornerSquared
#         shortcut =
#             shortcutCandidates
#                 |> List.filter (\textAndDistance -> textAndDistance.distanceUpperRightCornerSquared < 1000)
#                 |> List.head
#                 |> Maybe.map (\{ text } -> { text = text, parseResult = text |> parseModuleButtonTooltipShortcut })
#         optimalRangestr =
#             tooltipUINode.uiNode
#                 |> getAllContainedDisplayTexts
#                 |> List.filterMap
#                     (\text ->
#                         "Optimal range (|within)\\s*([\\d\\.]+\\s*[km]+)"
#                             |> Regex.fromstr
#                             |> Maybe.andThen (\regex -> text |> Regex.find regex |> List.head)
#                             |> Maybe.andThen (.submatches >> List.drop 1 >> List.head)
#                             |> Maybe.andThen identity
#                             |> Maybe.map str.trim
#                     )
#                 |> List.head
#         optimalRange =
#             optimalRangestr
#                 |> Maybe.map (\asstr -> { asstr = asstr, inMeters = asstr |> parseOverviewEntryDistanceInMetersFromText })
#     in
#     { uiNode = tooltipUINode
#     , shortcut = shortcut
#     , optimalRange = optimalRange
#     }


def parseModuleButtonTooltipShortcut(shortcutText: str) -> Union[str, List[CUSTOMKEYCODE]]:
    raise NotImplementedError()
# parseModuleButtonTooltipShortcut : str -> Result str (List Common.EffectOnWindow.VirtualKeyCode)
# parseModuleButtonTooltipShortcut shortcutText =
#     shortcutText
#         |> str.split "-"
#         |> List.concatMap (str.split "+")
#         |> List.map str.trim
#         |> List.filter (str.length >> (<) 0)
#         |> List.foldl
#             (\nextKeyText previousResult ->
#                 previousResult
#                     |> Result.andThen
#                         (\previousKeys ->
#                             case nextKeyText |> parseKeyShortcutText of
#                                 Just nextKey ->
#                                     Ok (nextKey :: previousKeys)
#                                 Nothing ->
#                                     Err ("Unknown key text: '" ++ nextKeyText ++ "'")
#                         )
#             )
#             (Ok [])
#         |> Result.map List.reverse


def parseKeyShortcutText(keytext: str) -> Optional[CUSTOMKEYCODE]:
    raise NotImplementedError()
# parseKeyShortcutText : str -> Maybe Common.EffectOnWindow.VirtualKeyCode
# parseKeyShortcutText keyText =
#     [ ( "CTRL", Common.EffectOnWindow.vkey_LCONTROL )
#     , ( "STRG", Common.EffectOnWindow.vkey_LCONTROL )
#     , ( "ALT", Common.EffectOnWindow.vkey_LMENU )
#     , ( "SHIFT", Common.EffectOnWindow.vkey_LSHIFT )
#     , ( "UMSCH", Common.EffectOnWindow.vkey_LSHIFT )
#     , ( "F1", Common.EffectOnWindow.vkey_F1 )
#     , ( "F2", Common.EffectOnWindow.vkey_F2 )
#     , ( "F3", Common.EffectOnWindow.vkey_F3 )
#     , ( "F4", Common.EffectOnWindow.vkey_F4 )
#     , ( "F5", Common.EffectOnWindow.vkey_F5 )
#     , ( "F6", Common.EffectOnWindow.vkey_F6 )
#     , ( "F7", Common.EffectOnWindow.vkey_F7 )
#     , ( "F8", Common.EffectOnWindow.vkey_F8 )
#     , ( "F9", Common.EffectOnWindow.vkey_F9 )
#     , ( "F10", Common.EffectOnWindow.vkey_F10 )
#     , ( "F11", Common.EffectOnWindow.vkey_F11 )
#     , ( "F12", Common.EffectOnWindow.vkey_F12 )
#     ]
#         |> Dict.fromList
#         |> Dict.get (keyText |> str.toUpper)


def parseChatWindowStacksFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[ChatWindowStack]:

    matches = (x for x in listDescendantsWithDisplayRegion(uiTreeRoot)
               if x.uiNode.pythonObjectTypeName == 'ChatWindowStack')
    return [parseChatWindowStack(x) for x in matches]
# parseChatWindowStacksFromUITreeRoot : UITreeNodeWithDisplayRegion -> List ChatWindowStack
# parseChatWindowStacksFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ChatWindowStack")
#         |> List.map parseChatWindowStack


def parseChatWindowStack(chatWindowStackUiNode: UITreeNodeWithDisplayRegion) -> ChatWindowStack:
    _s = [y for y in listDescendantsWithDisplayRegion(
        chatWindowStackUiNode) if y.uiNode.pythonObjectTypeName == 'XmppChatWindow']
    chatWindowNode = _s[0]
    result = ChatWindowStack()
    result.uiNode = chatWindowStackUiNode
    result.chatWindow = parseChatWindow(chatWindowNode)
    return result

# parseChatWindowStack : UITreeNodeWithDisplayRegion -> ChatWindowStack
# parseChatWindowStack chatWindowStackUiNode =
#     let
#         chatWindowNode =
#             chatWindowStackUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "XmppChatWindow")
#                 |> List.head
#     in
#     { uiNode = chatWindowStackUiNode
#     , chatWindow = chatWindowNode |> Maybe.map parseChatWindow
#     }


def parseChatWindow(chatWindowuiNode: UITreeNodeWithDisplayRegion) -> ChatWindow:
    userListNode: List[UITreeNodeWithDisplayRegion] = []
    keys = {}
    for x in listDescendantsWithDisplayRegion(chatWindowuiNode):
        _r = getNameFromDictEntries(x.uiNode)
        # print(_r)
        keys[x] = _r
        if _r is not None and 'userlist' == _r:
            userListNode.append(x)
    print("------------")
    print("Keys: ", keys.values())
    print(userListNode)
    _firstNode = userListNode[0]
    result = ChatWindow()
    result.uiNode = _firstNode
    result.name = keys[_firstNode]
    print("Name: ", result.name)
    result.userlist = parseChatWindowUserlist(_firstNode)
    return result
# parseChatWindow : UITreeNodeWithDisplayRegion -> ChatWindow
# parseChatWindow chatWindowUiNode =
#     let
#         userlistNode =
#             chatWindowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> getNameFromDictEntries >> Maybe.map (str.toLower >> str.contains "userlist") >> Maybe.withDefault False)
#                 |> List.head
#     in
#     { uiNode = chatWindowUiNode
#     , name = getNameFromDictEntries chatWindowUiNode.uiNode
#     , userlist = userlistNode |> Maybe.map parseChatWindowUserlist
#     }


def parseChatWindowUserlist(userListNode: UITreeNodeWithDisplayRegion) -> ChatWindowUserlist:
    # visibleUsers = [x for x in listDescendantsWithDisplayRegion(userListNode) if foldl()]
    visibleUsers = []
    scrollDisplayRegions = []
    for x in listDescendantsWithDisplayRegion(userListNode):
        if x.uiNode.pythonObjectTypeName in ['XmppChatSimpleUserEntry', 'XmppChatUserEntry']:
            # print("Raw: ", x.uiNode.pythonObjectTypeName, x.uiNode.pythonObjectAddress)
            _c = parseChatUserEntry(x)
            # print("_c", _c)
            visibleUsers.append(_c)
        if 'ScrollControls' in x.uiNode.pythonObjectTypeName:
            scrollDisplayRegions.append(x)
    scrollControls = parseScrollControls(scrollDisplayRegions[0]) if len(
        scrollDisplayRegions) > 0 else None
    result = ChatWindowUserlist()
    result.uiNode = userListNode
    result.visibleUsers = visibleUsers
    result.scrollControls = scrollControls
    return result
# parseChatWindowUserlist : UITreeNodeWithDisplayRegion -> ChatWindowUserlist
# parseChatWindowUserlist userlistNode =
#     let
#         visibleUsers =
#             userlistNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (\uiNode -> [ "XmppChatSimpleUserEntry", "XmppChatUserEntry" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#                 |> List.map parseChatUserEntry
#         scrollControls =
#             userlistNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "ScrollControls")
#                 |> List.head
#                 |> Maybe.map parseScrollControls
#     in
#     { uiNode = userlistNode, visibleUsers = visibleUsers, scrollControls = scrollControls }


def parseChatUserEntry(chatUserUiNode: UITreeNodeWithDisplayRegion) -> ChatUserEntry:
    # print("Testing List: ")
    # pprint(chatUserUiNode)
    # print(vars(chatUserUiNode))
    # print([x.uiNode.pythonObjectTypeName for x in listDescendantsWithDisplayRegion(chatUserUiNode)])
    # print("Done.")

    standingIconNodes = [x for x in listDescendantsWithDisplayRegion(
        chatUserUiNode) if x.uiNode.pythonObjectTypeName == 'FlagIconWithState']
    # print(standingIconNodes)
    standingIconNode = standingIconNodes[0] if len(
        standingIconNodes) > 0 else None
    names = [x for x in getAllContainedDisplayTexts(
        chatUserUiNode.uiNode) if x is not None]
    names.sort(key=len, reverse=True)
    # print("Names: " , names)
    name = names[0]
    standingIconHint = None
    if standingIconNode is not None:
        standingIconHint = getHintTextFromDictEntries(standingIconNode.uiNode)
    result = ChatUserEntry()
    result.name = name
    result.standingIconHint = standingIconHint
    result.uiNode = chatUserUiNode
    return result

# parseChatUserEntry : UITreeNodeWithDisplayRegion -> ChatUserEntry
# parseChatUserEntry chatUserUiNode =
#     let
#         standingIconNode =
#             chatUserUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FlagIconWithState")
#                 |> List.head
#         name =
#             chatUserUiNode.uiNode
#                 |> getAllContainedDisplayTexts
#                 |> List.sortBy str.length
#                 |> List.reverse
#                 |> List.head
#         standingIconHint =
#             standingIconNode
#                 |> Maybe.andThen (.uiNode >> getHintTextFromDictEntries)
#     in
#     { uiNode = chatUserUiNode
#     , name = name
#     , standingIconHint = standingIconHint
#     }


def parseAgentConversationWindowsFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[AgentConversationWindow]:
    raise NotImplementedError()
# parseAgentConversationWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List AgentConversationWindow
# parseAgentConversationWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AgentDialogueWindow")
#         |> List.map parseAgentConversationWindow


def parseAgentConversationWindow(windowUINode: UITreeNodeWithDisplayRegion) -> AgentConversationWindow:
    raise NotImplementedError()
# parseAgentConversationWindow : UITreeNodeWithDisplayRegion -> AgentConversationWindow
# parseAgentConversationWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseMarketOrdersWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[MarketOrdersWindow]:
    raise NotImplementedError()
# parseMarketOrdersWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe MarketOrdersWindow
# parseMarketOrdersWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MarketOrdersWnd")
#         |> List.head
#         |> Maybe.map parseMarketOrdersWindow


def parseMarketOrdersWindow(windowUINode: UITreeNodeWithDisplayRegion) -> MarketOrdersWindow:
    raise NotImplementedError()
# parseMarketOrdersWindow : UITreeNodeWithDisplayRegion -> MarketOrdersWindow
# parseMarketOrdersWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseFittingWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[FittingWindow]:
    raise NotImplementedError()
# parseFittingWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FittingWindow
# parseFittingWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FittingWindow")
#         |> List.head
#         |> Maybe.map parseFittingWindow


def parseFittingWindow(windowUINode: UITreeNodeWithDisplayRegion) -> FittingWindow:
    raise NotImplementedError()
# parseFittingWindow : UITreeNodeWithDisplayRegion -> FittingWindow
# parseFittingWindow windowUINode =
#     { uiNode = windowUINode
#     }


def parseSurveyScanWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[SurveyScanWindow]:
    raise NotImplementedError()
# parseSurveyScanWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SurveyScanWindow
# parseSurveyScanWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanView")
#         |> List.head
#         |> Maybe.map parseSurveyScanWindow


def parseSurveyScanWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> SurveyScanWindow:
    raise NotImplementedError()
# parseSurveyScanWindow : UITreeNodeWithDisplayRegion -> SurveyScanWindow
# parseSurveyScanWindow windowUINode =
#     { uiNode = windowUINode
#     , scanEntries =
#         windowUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanEntry")
#     }


def parseBookmarkLocationWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[BookmarkLocationWindow]:
    data = [parseBookmarkLocationWindow(x) for x in listDescendantsWithDisplayRegion(uiTreeRoot) if x.uiNode.pythonObjectTypeName == 'BookmarkLocationWindow']
    return None if len(data) == 0 else data[0]
# parseBookmarkLocationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe BookmarkLocationWindow
# parseBookmarkLocationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "BookmarkLocationWindow")
#         |> List.head
#         |> Maybe.map parseBookmarkLocationWindow


def parseBookmarkLocationWindow(windowUINode: UITreeNodeWithDisplayRegion) -> BookmarkLocationWindow:
    def buttonFromLabelText(labelText: str) -> UITreeNodeWithDisplayRegion:
        data = [x for x in listDescendantsWithDisplayRegion(windowUINode) if 'Button' in x.uiNode.pythonObjectTypeNam and labelText.lower() in [y.strip().lower() for y in getAllContainedDisplayTexts(x.uiNode)]]
        data.sort( key=lambda x: areaFromDisplayRegion(x.totalDisplayRegion) or 0)
        return data[0]
    r = BookmarkLocationWindow()
    r.uiNode = windowUINode
    r.cancelButton = buttonFromLabelText('cancel')
    r.submitButton = buttonFromLabelText('submit')
    return r
    
# parseBookmarkLocationWindow : UITreeNodeWithDisplayRegion -> BookmarkLocationWindow
# parseBookmarkLocationWindow windowUINode =
#     let
#         buttonFromLabelText labelText =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Button")
#                 |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.trim >> str.toLower) >> List.member (labelText |> str.toLower))
#                 |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.head
#     in
#     { uiNode = windowUINode
#     , submitButton = buttonFromLabelText "submit"
#     , cancelButton = buttonFromLabelText "cancel"
#     }


def parseRepairShopWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[RepairShopWindow]:
    raise NotImplementedError()
# parseRepairShopWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe RepairShopWindow
# parseRepairShopWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "RepairShopWindow")
#         |> List.head
#         |> Maybe.map parseRepairShopWindow


def parseRepairShopWindow(windowUINode: UITreeNodeWithDisplayRegion) -> RepairShopWindow:
    raise NotImplementedError()
# parseRepairShopWindow : UITreeNodeWithDisplayRegion -> RepairShopWindow
# parseRepairShopWindow windowUINode =
#     let
#         buttonFromLabelText labelText =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "Button")
#                 |> List.filter (.uiNode >> getAllContainedDisplayTexts >> List.map (str.trim >> str.toLower) >> List.member (labelText |> str.toLower))
#                 |> List.sortBy (.totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                 |> List.head
#     in
#     { uiNode = windowUINode
#     , items =
#         windowUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Item")
#     , repairItemButton = buttonFromLabelText "repair item"
#     , pickNewItemButton = buttonFromLabelText "pick new item"
#     , repairAllButton = buttonFromLabelText "repair all"
#     }


def parseCharacterSheetWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[CharacterSheetWindow]:
    raise NotImplementedError()
# parseCharacterSheetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe CharacterSheetWindow
# parseCharacterSheetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "CharacterSheetWindow")
#         |> List.head
#         |> Maybe.map parseCharacterSheetWindow


def parseCharacterSheetWindow(windowUINode: UITreeNodeWithDisplayRegion) -> CharacterSheetWindow:
    raise NotImplementedError()
# parseCharacterSheetWindow : UITreeNodeWithDisplayRegion -> CharacterSheetWindow
# parseCharacterSheetWindow windowUINode =
#     let
#         skillGroups =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> str.contains "SkillGroupGauge")
#     in
#     { uiNode = windowUINode
#     , skillGroups = skillGroups
#     }


def parseFleetWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[FleetWindow]:
    raise NotImplementedError()
# parseFleetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FleetWindow
# parseFleetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FleetWindow")
#         |> List.head
#         |> Maybe.map parseFleetWindow


def parseFleetwindow(windowUINode: UITreeNodeWithDisplayRegion) -> FleetWindow:
    raise NotImplementedError()
# parseFleetWindow : UITreeNodeWithDisplayRegion -> FleetWindow
# parseFleetWindow windowUINode =
#     let
#         fleetMembers =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FleetMember")
#     in
#     { uiNode = windowUINode
#     , fleetMembers = fleetMembers
#     }


def parseWatchListPanelFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[WatchListPanel]:
    raise NotImplementedError()
# parseWatchListPanelFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe WatchListPanel
# parseWatchListPanelFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "WatchListPanel")
#         |> List.head
#         |> Maybe.map parseWatchListPanel


def parseWatchListPanel(windowUINode: UITreeNodeWithDisplayRegion) -> WatchListPanel:
    raise NotImplementedError()
# parseWatchListPanel : UITreeNodeWithDisplayRegion -> WatchListPanel
# parseWatchListPanel windowUINode =
#     let
#         entries =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "WatchListEntry")
#     in
#     { uiNode = windowUINode
#     , entries = entries
#     }


def parseStandaloneBookmarkWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[StandaloneBookmarkWindow]:
    raise NotImplementedError()
# parseStandaloneBookmarkWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe StandaloneBookmarkWindow
# parseStandaloneBookmarkWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "StandaloneBookmarkWnd")
#         |> List.head
#         |> Maybe.map parseStandaloneBookmarkWindow


def parseStandaloneBookmarkWindow(windowUINode: UITreeNodeWithDisplayRegion) -> StandaloneBookmarkWindow:
    raise NotImplementedError()
# parseStandaloneBookmarkWindow : UITreeNodeWithDisplayRegion -> StandaloneBookmarkWindow
# parseStandaloneBookmarkWindow windowUINode =
#     let
#         entries =
#             windowUINode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "PlaceEntry")
#     in
#     { uiNode = windowUINode
#     , entries = entries
#     }


def parseNeocomFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[Neocom]:
    raise NotImplementedError()
# parseNeocomFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe Neocom
# parseNeocomFromUITreeRoot uiTreeRoot =
#     case
#         uiTreeRoot
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Neocom")
#             |> List.head
#     of
#         Nothing ->
#             Nothing
#         Just uiNode ->
#             Just (parseNeocom uiNode)


def parseNeocom(neocomUiNode: UITreeNodeWithDisplayRegion) -> Neocom:
    raise NotImplementedError()
# parseNeocom : UITreeNodeWithDisplayRegion -> Neocom
# parseNeocom neocomUiNode =
#     let
#         maybeClockTextAndNode =
#             neocomUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "InGameClock")
#                 |> List.concatMap getAllContainedDisplayTextsWithRegion
#                 |> List.head
#         nodeFromTexturePathEnd texturePathEnd =
#             neocomUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter
#                     (.uiNode
#                         >> getTexturePathFromDictEntries
#                         >> Maybe.map (str.endsWith texturePathEnd)
#                         >> Maybe.withDefault False
#                     )
#                 |> List.head
#         clock =
#             maybeClockTextAndNode
#                 |> Maybe.map
#                     (\( clockText, clockNode ) ->
#                         { uiNode = clockNode
#                         , text = clockText
#                         , parsedText = parseNeocomClockText clockText
#                         }
#                     )
#     in
#     { uiNode = neocomUiNode
#     , iconInventory = nodeFromTexturePathEnd "items.png"
#     , clock = clock
#     }


def parseNeocomClockText(clockText: str) -> Union[str, ParsedTime]:
    raise NotImplementedError()
# parseNeocomClockText : str -> Result str { hour : int, minute : int }
# parseNeocomClockText clockText =
#     case clockText |> str.split ":" of
#         [ hourText, minuteText ] ->
#             case hourText |> str.trim |> str.toint of
#                 Nothing ->
#                     Err ("Failed to parse hour: '" ++ hourText ++ "'")
#                 Just hour ->
#                     case minuteText |> str.trim |> str.toint of
#                         Nothing ->
#                             Err ("Failed to parse minute: '" ++ minuteText ++ "'")
#                         Just minute ->
#                             Ok { hour = hour, minute = minute }
#         _ ->
#             Err "Expecting exactly two substrs separated by a colon (:)."


def parseKeyActivationWindowFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[KeyActivationWindow]:
    raise NotImplementedError()
# parseKeyActivationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe KeyActivationWindow
# parseKeyActivationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "KeyActivationWindow")
#         |> List.head
#         |> Maybe.map parseKeyActivationWindow


def parseKeyActiationWindow(windowUiNode: UITreeNodeWithDisplayRegion) -> KeyActivationWindow:
    raise NotImplementedError()
# parseKeyActivationWindow : UITreeNodeWithDisplayRegion -> KeyActivationWindow
# parseKeyActivationWindow windowUiNode =
#     let
#         activateButton =
#             windowUiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ActivateButton")
#                 |> List.head
#     in
#     { uiNode = windowUiNode
#     , activateButton = activateButton
#     }


def parseExpander(uiNode: UITreeNodeWithDisplayRegion) -> Expander:
    raise NotImplementedError()
# parseExpander : UITreeNodeWithDisplayRegion -> Expander
# parseExpander uiNode =
#     let
#         maybeTexturePath =
#             getTexturePathFromDictEntries uiNode.uiNode
#         isExpanded =
#             maybeTexturePath
#                 |> Maybe.andThen
#                     (\texturePath ->
#                         [ ( "38_16_228.png", False ), ( "38_16_229.png", True ) ]
#                             |> List.filter (\( pathEnd, _ ) -> texturePath |> str.endsWith pathEnd)
#                             |> List.map Tuple.second
#                             |> List.head
#                     )
#     in
#     { uiNode = uiNode
#     , texturePath = maybeTexturePath
#     , isExpanded = isExpanded
#     }


def parseMessageBoxesFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> List[MessageBox]:
    raise NotImplementedError()
# parseMessageBoxesFromUITreeRoot : UITreeNodeWithDisplayRegion -> List MessageBox
# parseMessageBoxesFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MessageBox")
#         |> List.map parseMessageBox


def parseMessageBox(uiNode: UITreeNodeWithDisplayRegion) -> MessageBox:
    raise NotImplementedError()
# parseMessageBox : UITreeNodeWithDisplayRegion -> MessageBox
# parseMessageBox uiNode =
#     let
#         buttons =
#             uiNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "Button")
#                 |> List.map
#                     (\buttonNode ->
#                         { uiNode = buttonNode
#                         , maintext =
#                             buttonNode
#                                 |> getAllContainedDisplayTextsWithRegion
#                                 |> List.sortBy (Tuple.second >> .totalDisplayRegion >> areaFromDisplayRegion >> Maybe.withDefault 0)
#                                 |> List.map Tuple.first
#                                 |> List.head
#                         }
#                     )
#     in
#     { buttons = buttons
#     , uiNode = uiNode
#     }


def parseScrollControls(scrollControlsNode: UITreeNodeWithDisplayRegion) -> ScrollControls:
    scrollHandles = [x for x in listDescendantsWithDisplayRegion(
        scrollControlsNode) if x.uiNode.pythonObjectTypeName == 'ScrollHandle']
    scrollHandle = scrollHandles[0]
    sc = ScrollControls()
    sc.scrollHandle = scrollHandle
    sc.uiNode = scrollControlsNode
    return sc
# parseScrollControls : UITreeNodeWithDisplayRegion -> ScrollControls
# parseScrollControls scrollControlsNode =
#     let
#         scrollHandle =
#             scrollControlsNode
#                 |> listDescendantsWithDisplayRegion
#                 |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ScrollHandle")
#                 |> List.head
#     in
#     { uiNode = scrollControlsNode
#     , scrollHandle = scrollHandle
#     }


def parseLayerAbovemainFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[UITreeNodeWithDisplayRegion]:
    raise NotImplementedError()
# parseLayerAbovemainFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe UITreeNodeWithDisplayRegion
# parseLayerAbovemainFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "l_abovemain"))
#         |> List.head


def getSubstrBetweenXmlTagsAfterMarker(marker: str) -> Callable[[str], Optional[str]]:
    raise NotImplementedError()

    def fn(x: str) -> Optional[str]:
        raise NotImplementedError()
    return fn
# getSubstrBetweenXmlTagsAfterMarker : str -> str -> Maybe str
# getSubstrBetweenXmlTagsAfterMarker marker =
#     str.split marker
#         >> List.drop 1
#         >> List.head
#         >> Maybe.andThen (str.split ">" >> List.drop 1 >> List.head)
#         >> Maybe.andThen (str.split "<" >> List.head)


def parseNumberTruncatingAfterOptionalDecimalSeparator(numberDisplayText: str) -> Union[str, int]:
    raise NotImplementedError()
# parseNumberTruncatingAfterOptionalDecimalSeparator : str -> Result str int
# parseNumberTruncatingAfterOptionalDecimalSeparator numberDisplayText =
#     let
#         expectedSeparators =
#             [ ",", ".", "???", " ", "\u{00A0}", "\u{202F}" ]
#         groupsTexts =
#             expectedSeparators
#                 |> List.foldl (\separator -> List.concatMap (str.split separator))
#                     [ str.trim numberDisplayText ]
#         lastGroupIsFraction =
#             case List.reverse groupsTexts of
#                 lastGroupText :: _ :: _ ->
#                     str.length lastGroupText < 3
#                 _ ->
#                     False
#         integerText =
#             str.join ""
#                 (if lastGroupIsFraction then
#                     groupsTexts |> List.reverse |> List.drop 1 |> List.reverse
#                  else
#                     groupsTexts
#                 )
#     in
#     integerText
#         |> str.toint
#         |> Result.fromMaybe ("Failed to parse to integer: " ++ integerText)


def centerFromDisplayRegion(region: DisplayRegion) -> Location2d:
    raise NotImplementedError()
# centerFromDisplayRegion : DisplayRegion -> Location2d
# centerFromDisplayRegion region =
#     { x = region.x + region.width // 2, y = region.y + region.height // 2 }


def getDisplayText(uiNode: UITreeNode) -> Optional[str]:
    _s = ('_setText', '_text')
    for s in _s:
        _n = uiNode.dictEntriesOfInterest.get(s, None)
        if _n is not None:
            return _n
    return None
# getDisplayText : UITreeNode -> Maybe str
# getDisplayText uiNode =
#     [ "_setText", "_text" ]
#         |> List.filterMap
#             (\displayTextPropertyName ->
#                 uiNode.dictEntriesOfinterest
#                     |> Dict.get displayTextPropertyName
#                     |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.str >> Result.toMaybe)
#             )
#         |> List.sortBy (str.length >> negate)
#         |> List.head


def getAllContainedDisplayTexts(uiNode: UITreeNode) -> List[str]:
    _list = [uiNode]
    _decendants = listDescendantsInUITreeNode(uiNode)
    if _decendants is not None:
        _list.extend(_decendants)
    _data = [getDisplayText(x) for x in _list if x is not None]
    return [x for x in _data if x is not None]
# getAllContainedDisplayTexts : UITreeNode -> List str
# getAllContainedDisplayTexts uiNode =
#     uiNode
#         :: (uiNode |> listDescendantsInUITreeNode)
#         |> List.filterMap getDisplayText


def getAllContainedDisplayTextsWithRegion(uiNode: UITreeNodeWithDisplayRegion) -> List[Tuple[str, UITreeNodeWithDisplayRegion]]:
    raise NotImplementedError()

# getAllContainedDisplayTextsWithRegion : UITreeNodeWithDisplayRegion -> List ( str, UITreeNodeWithDisplayRegion )
# getAllContainedDisplayTextsWithRegion uiNode =
#     uiNode
#         :: (uiNode |> listDescendantsWithDisplayRegion)
#         |> List.filterMap
#             (\descendant ->
#                 let
#                     displayText =
#                         descendant.uiNode |> getDisplayText |> Maybe.withDefault ""
#                 in
#                 if 0 < (displayText |> str.length) then
#                     Just ( displayText, descendant )
#                 else
#                     Nothing
#             )


def getNameFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get("_name")
# getNameFromDictEntries : UITreeNode -> Maybe str
# getNameFromDictEntries =
#     getstrPropertyFromDictEntries "_name"


def getHintTextFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get("_hint")
# getHintTextFromDictEntries : UITreeNode -> Maybe str
# getHintTextFromDictEntries =
#     getstrPropertyFromDictEntries "_hint"


def getTexturePathFromDictEntries(x: UITreeNode) -> Optional[str]:
    return x.dictEntriesOfInterest.get('texturePath')
# getTexturePathFromDictEntries : UITreeNode -> Maybe str
# getTexturePathFromDictEntries =
#     getstrPropertyFromDictEntries "texturePath"


# def getstrPropertyFromDictEntries(dictEntryKey: str) -> Callable[[UITreeNode], Optional[str]]:
#     def fn(x: UITreeNode) -> Optional[str]:
#         raise NotImplementedError()
#     return fn
# getstrPropertyFromDictEntries : str -> UITreeNode -> Maybe str
# getstrPropertyFromDictEntries dictEntryKey uiNode =
#     uiNode.dictEntriesOfinterest
#         |> Dict.get dictEntryKey
#         |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.str >> Result.toMaybe)


def getColorPercentFromDictEntries(x: UITreeNode) -> Optional[ColorComponents]:
    return jsonDecodeColorPercent(x.dictEntriesOfInterest.get('_color'))

# getColorPercentFromDictEntries : UITreeNode -> Maybe ColorComponents
# getColorPercentFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_color"
#         >> Maybe.andThen (Json.Decode.decodeValue jsonDecodeColorPercent >> Result.toMaybe)


def jsonDecodeColorPercent(x: Dict) -> Optional[ColorComponents]:
    print("jsonDecodeColorPercent", x)
    _c = ColorComponents()
    try:
        _c.a = x.get('aPercent')
        _c.r = x.get('rPercent')
        _c.g = x.get('gPercent')
        _c.b = x.get('bPercent')
    except:
        return None
    if None in [_c.a, _c.r, _c.b, _c.g]:
        return None
    return _c

# jsonDecodeColorPercent : Json.Decode.Decoder ColorComponents
# jsonDecodeColorPercent =
#     Json.Decode.map4 ColorComponents
#         (Json.Decode.field "aPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "rPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "gPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "bPercent" jsonDecodeintFromintOrstr)


def getRotationFloatFromDictEntries(x: UITreeNode) -> Optional[float]:
    try:
        return float(x.dictEntriesOfInterest.get('_rotation'))
    except:
        return None
# getRotationFloatFromDictEntries : UITreeNode -> Maybe Float
# getRotationFloatFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_rotation"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)


def jsonDecodeintFromintOrstr(x):
    try:
        return int(x)
    except Exception as e:
        print("Exception: jsonDecodeintFromintOrstr ", e)
        raise e
# jsonDecodeintFromintOrstr : Json.Decode.Decoder int
# jsonDecodeintFromintOrstr =
#     Json.Decode.oneOf
#         [ Json.Decode.int
#         , Json.Decode.str
#             |> Json.Decode.andThen
#                 (\asstr ->
#                     case asstr |> str.toint of
#                         Just asint ->
#                             Json.Decode.succeed asint
#                         Nothing ->
#                             Json.Decode.fail ("Failed to parse integer from str '" ++ asstr ++ "'")
#                 )
#         ]


def getHorizontalOffsetFromParentAndWidth(uiNode: UITreeNode) -> Optional[OffsetWidth]:
    def roundedNumberFromPropertyName(propertyName: str) -> float:
        try:
            return float(uiNode.dictEntriesOfInterest.get(propertyName))
        except Exception as e:
            print("Exception caught in getHorizontalOffsetFromParentAndWidth: ", e)
            raise e
    try:
        x = round(roundedNumberFromPropertyName('_displayX'))
        w = round(roundedNumberFromPropertyName('_width'))
        ow = OffsetWidth(x, w)
        return ow
    except Exception as e:
        return None


# getHorizontalOffsetFromParentAndWidth : UITreeNode -> Maybe { offset : int, width : int }
# getHorizontalOffsetFromParentAndWidth uiNode =
#     let
#         roundedNumberFromPropertyName propertyName =
#             uiNode.dictEntriesOfinterest
#                 |> Dict.get propertyName
#                 |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#                 |> Maybe.map round
#     in
#     case ( roundedNumberFromPropertyName "_displayX", roundedNumberFromPropertyName "_width" ) of
#         ( Just offset, Just width ) ->
#             Just { offset = offset, width = width }
#         _ ->
#             Nothing


def areaFromDisplayRegion(region: DisplayRegion) -> Optional[int]:
    if region.width < 0 or region.height < 0:
        return None
    return region.width * region.height
# areaFromDisplayRegion : DisplayRegion -> Maybe int
# areaFromDisplayRegion region =
#     if region.width < 0 || region.height < 0 then
#         Nothing
#     else
#         Just (region.width * region.height)


def getVerticalOffsetFromParent(x: UITreeNode) -> Optional[int]:
    try:
        return int(x.dictEntriesOfInterest.get('_displayY'))
    except Exception as e:
        print("Exception Caught in getverticalOffsetFromParent: ", e)
    return None


# getVerticalOffsetFromParent : UITreeNode -> Maybe int
# getVerticalOffsetFromParent =
#     .dictEntriesOfinterest
#         >> Dict.get "_displayY"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#         >> Maybe.map round


def getMostPopulousDescendantMatchingPredicate(uiTreeNode: UITreeNode, parent: UITreeNode) -> Optional[UITreeNode]:
    raise NotImplementedError()
    # listDescendantsInUITreeNode(parent)
# getMostPopulousDescendantMatchingPredicate : (UITreeNode -> bool) -> UITreeNode -> Maybe UITreeNode
# getMostPopulousDescendantMatchingPredicate predicate parent =
#     listDescendantsInUITreeNode parent
#         |> List.filter predicate
#         |> List.sortBy countDescendantsInUITreeNode
#         |> List.reverse
#         |> List.head


def listDescendantsInUITreeNode(parent: UITreeNode) -> List[UITreeNode]:
    _p = parent.children or []
    _r = [unwrapUITreeNodeChild(x) for x in _p]
    result: List[UITreeNode] = []
    for x in _r:
        result.append(x)
        result.extend(listDescendantsInUITreeNode(x))
    return result

# listDescendantsInUITreeNode : UITreeNode -> List UITreeNode
# listDescendantsInUITreeNode parent =
#     parent.children
#         |> Maybe.withDefault []
#         |> List.map unwrapUITreeNodeChild
#         |> List.concatMap (\child -> child :: listDescendantsInUITreeNode child)


def listDescendantsWithDisplayRegion(parent: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    result = []
    # print("listDecesnatsWithDisplayRegion")
    # pprint(parent)
    for child in listChildrenWithDisplayRegion(parent):
        # print("Child Address: ", child.uiNode.pythonObjectAddress)
        result.append(child)
        result.extend(listDescendantsWithDisplayRegion(child))
    # print("ListDescendantsWithDisplayRegion :", result)
    return result

# listDescendantsWithDisplayRegion : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# listDescendantsWithDisplayRegion parent =
#     parent
#         |> listChildrenWithDisplayRegion
#         |> List.concatMap (\child -> child :: listDescendantsWithDisplayRegion child)


def listChildrenWithDisplayRegion(parent: UITreeNodeWithDisplayRegion) -> List[UITreeNodeWithDisplayRegion]:
    # print("Child Nodes: ", parent.children)
    d = parent.children or []
    # print("D: ", [type(child) for child in d])
    return [child for child in d if type(child) == UITreeNodeWithDisplayRegion]

# listChildrenWithDisplayRegion : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# listChildrenWithDisplayRegion parent =
#     parent.children
#         |> Maybe.withDefault []
#         |> List.filterMap
#             (\child ->
#                 case child of
#                     ChildWithoutRegion _ ->
#                         Nothing
#                     ChildWithRegion childWithRegion ->
#                         Just childWithRegion
#             )
