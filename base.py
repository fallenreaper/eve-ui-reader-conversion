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

from contextvars import Context
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Set, Union


# Not Sure what this means at the common. Will need to check into it.
#  Wraping in a Try-Except in order to catch until I determine what it is.
try:
    CUSTOMKEYCODE = Common.EffectOnWindow.VirtualKeyCode
except:
    CUSTOMKEYCODE = None


class UITreeNode:
    pass


class DisplayRegion:
    x: int
    y: int
    width: int
    height: int


class ChildOfNodeWithDisplayRegion(Enum):
    ChildWithRegion = None  # UITreeNodeWithDisplayRegion
    ChildWithoutRegion = UITreeNode


class UITreeNodeWithDisplayRegion:
    uiNode: UITreeNode
    children: Optional[List[ChildOfNodeWithDisplayRegion]]
    selfDisplayRegion: DisplayRegion
    totalDisplayRegion: DisplayRegion


class Location2d:
    x: int
    y: int


class ColorComponents:
    a: int
    r: int
    g: int
    b: int


class ContextMenuEntry:
    uiNode: UITreeNodeWithDisplayRegion
    text: str


class ContextMenu:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[ContextMenuEntry]


class ShipUIModuleButton:
    uiNode: UITreeNodeWithDisplayRegion
    slotUINode: UITreeNodeWithDisplayRegion
    isActive: Optional[bool]
    isHiliteVisible: bool
    rampRotationMilli: Optional[int]


class ModuleRows(NamedTuple):
    top: List[ShipUIModuleButton]
    middle: List[ShipUIModuleButton]
    bottom: List[ShipUIModuleButton]


class Hitpoints:
    structure: int
    armor: int
    shield: int


class SquadronAbilityIcon:
    uiNode: UITreeNodeWithDisplayRegion
    quantity: Optional[int]
    ramp_active: Optional[bool]


class SquadronUI:
    uiNode: UITreeNodeWithDisplayRegion
    abilities: List[SquadronAbilityIcon]
    actionLabel: Optional[UITreeNodeWithDisplayRegion]


class SquadronsUI:
    uiNode: UITreeNodeWithDisplayRegion
    squadrons: List[SquadronUI]


class ShipUICapacitorPmark:
    uiNode: UITreeNodeWithDisplayRegion
    colorPercent: Optional[ColorComponents]


class ShipUICapacitor:
    uiNode: UITreeNodeWithDisplayRegion
    pmarks: List[ShipUICapacitorPmark]
    levelFromPmarksPercent: Optional[int]


class ShipManeuverType(Enum):
    ManeuverWarp = 0,
    ManeuverJump = 1,
    ManeuverOrbit = 2,
    ManeuverApproach = 3


class ShipUIIndication:
    uiNode: UITreeNodeWithDisplayRegion
    maneuverType: Optional[ShipManeuverType]


class ShipUI:
    uiNode: UITreeNodeWithDisplayRegion
    capacitor: ShipUICapacitor
    hitpointsPercent: Hitpoints
    indication: Optional[ShipUIIndication]
    moduleButtons: List[ShipUIModuleButton]
    moduleButtonsRows: ModuleRows

    offensiveBuffButtonNames: List[str]
    squadronsUI: Optional[SquadronsUI]
    stopButton: Optional[UITreeNodeWithDisplayRegion]
    maxSpeedButton: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelIcons:
    uiNode: UITreeNodeWithDisplayRegion
    search: Optional[UITreeNodeWithDisplayRegion]
    locationInfo: Optional[UITreeNodeWithDisplayRegion]
    route: Optional[UITreeNodeWithDisplayRegion]
    agentMissions: Optional[UITreeNodeWithDisplayRegion]
    dailyChallenge: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelRouteRouteElementMarker:
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelRoute:
    uiNode: UITreeNodeWithDisplayRegion
    routeElementMarker: List[InfoPanelRouteRouteElementMarker]


class InfoPanelLocationInfoExpandedContent:
    currentStationName: Optional[str]


class InfoPanelLocationInfo:
    uiNode: UITreeNodeWithDisplayRegion
    listSurroundingsButton: UITreeNodeWithDisplayRegion
    currentSolarSystemName: Optional[str]
    securityStatusPercent: Optional[int]
    expandedContent: Optional[InfoPanelLocationInfoExpandedContent]


class InfoPanelAgentMissionsEntry:
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelAgentMissions:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[InfoPanelAgentMissionsEntry]


class InfoPanelContainer:
    uiNode: UITreeNodeWithDisplayRegion
    icons: Optional[InfoPanelIcons]
    infoPanelLocationInfo: Optional[InfoPanelLocationInfo]
    infoPanelRoute: Optional[InfoPanelRoute]
    infoPanelAgentMissions: Optional[InfoPanelAgentMissions]


class Target:
    uiNode: UITreeNodeWithDisplayRegion
    barAndImageCont: Optional[UITreeNodeWithDisplayRegion]
    textsTopToBottom: List[str]
    isActiveTarget: bool
    assignedContainerNode: Optional[UITreeNodeWithDisplayRegion]
    assignedIcons: List[UITreeNodeWithDisplayRegion]


class OverviewWindowEntryCommonIndications:
    targeting: bool
    targetedByMe: bool
    isJammingMe: bool
    isWarpDisruptingMe: bool


class OverviewWindowEntry:
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    objectDistance: Optional[str]
    objectDistanceInMeters: Union[str, int]
    objectName: Optional[str]
    objectType: Optional[str]
    objectAlliance: Optional[str]
    iconSpriteColorPercent: Optional[ColorComponents]
    namesUnderSpaceObjectIcon: Set[str]
    bgColorFillsPercent: List[ColorComponents]
    rightAlignedIconsHints: List[str]
    commonIndications: OverviewWindowEntryCommonIndications


class ScrollControls:
    uiNode: UITreeNodeWithDisplayRegion
    scrollHandle: Optional[UITreeNodeWithDisplayRegion]


class OverviewWindow:
    uiNode: UITreeNodeWithDisplayRegion
    entriesHeaders: List[Union[str, UITreeNodeWithDisplayRegion]]
    entries: List[OverviewWindowEntry]
    scrollControls: Optional[ScrollControls]


class SelectedItemWindow:
    uiNode: UITreeNodeWithDisplayRegion
    orbitButton: Optional[UITreeNodeWithDisplayRegion]


class FittingWindow:
    uiNode: UITreeNodeWithDisplayRegion


class MarketOrdersWindow:
    uiNode: UITreeNodeWithDisplayRegion


class SurveyScanWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scanEntries: List[UITreeNodeWithDisplayRegion]


class RepairShopWindow:
    uiNode: UITreeNodeWithDisplayRegion
    items: List[UITreeNodeWithDisplayRegion]
    repairItemButton: Optional[UITreeNodeWithDisplayRegion]
    pickNewItemButton: Optional[UITreeNodeWithDisplayRegion]
    repairAllButton: Optional[UITreeNodeWithDisplayRegion]


class CharacterSheetWindow:
    uiNode: UITreeNodeWithDisplayRegion
    skillGroups: List[UITreeNodeWithDisplayRegion]


class Expander:
    uiNode: UITreeNodeWithDisplayRegion
    texturePath: Optional[str]
    isExpanded: Optional[bool]


class DronesWindowDroneGroupHeader:
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    expander: Expander
    quantityFromTitle: Optional[int]


class DronesWindowEntryGroupStructure:
    header: DronesWindowDroneGroupHeader
    children: List[Any]  # DronesWindowEntry


class DronesWindowEntryDroneStructure:
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    hitpointsPercent: Optional[Hitpoints]


class DronesWindowEntry(Enum):
    DronesWindowEntryGroup = DronesWindowEntryGroupStructure
    DronesWindowEntryDrone = DronesWindowEntryDroneStructure


class DronesWindow:
    uiNode: UITreeNodeWithDisplayRegion
    droneGroups: List[DronesWindowEntryGroupStructure]
    droneGroupInBay: Optional[DronesWindowEntryGroupStructure]
    droneGroupInLocalSpace: Optional[DronesWindowEntryGroupStructure]


class ProbeScanResult:
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    warpButton: Optional[UITreeNodeWithDisplayRegion]


class ProbeScannerWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scanResults: List[ProbeScanResult]


class DirectionalScannerWindow:
    uiNode: UITreeNodeWithDisplayRegion
    scrollNode: Optional[UITreeNodeWithDisplayRegion]
    scanResults: List[UITreeNodeWithDisplayRegion]


class StationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    undockButton: Optional[UITreeNodeWithDisplayRegion]
    abortUndockButton: Optional[UITreeNodeWithDisplayRegion]


class InventoryWindowLeftTreeEntryChild:
    InventoryWindowLeftTreeEntryChild: Any  # InventoryWindowLeftTreeEntry


class InventoryWindowLeftTreeEntry:
    uiNode: UITreeNodeWithDisplayRegion
    toggleBtn: Optional[UITreeNodeWithDisplayRegion]
    selectRegion: Optional[UITreeNodeWithDisplayRegion]
    text: str
    children: List[InventoryWindowLeftTreeEntryChild]


class InventoryWindowCapacityGauge:
    used: int
    maximum: Optional[int]
    selected: Optional[int]


class Items:
    items: List[UITreeNodeWithDisplayRegion]


class InventoryItemsView(Enum):
    InventoryItemsListView = Items
    InventoryItemsNotListView = Items


class Inventory:
    uiNode: UITreeNodeWithDisplayRegion
    itemsView: Optional[InventoryItemsView]
    scrollControls: Optional[ScrollControls]


class InventoryWindow:
    uiNode: UITreeNodeWithDisplayRegion
    leftTreeEntries: List[InventoryWindowLeftTreeEntry]
    subCaptionLabelText: Optional[str]
    selectedContainerCapacityGauge: Optional[Union[str,
                                                   InventoryWindowCapacityGauge]]
    selectedContainerInventory: Optional[Inventory]
    buttonToSwitchToListView: Optional[UITreeNodeWithDisplayRegion]


class ChatUserEntry:
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    standingIconHint: Optional[str]


class ShortCut(NamedTuple):
    text: str
    parseResult: Optional[Union[str, List[CUSTOMKEYCODE]]]


class ChatWindowUserlist:
    uiNode: UITreeNodeWithDisplayRegion
    visibleUsers: List[ChatUserEntry]
    scrollControls: Optional[ScrollControls]


class ChatWindow:
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    user: Optional[ChatWindowUserlist]


class ChatWindowStack:
    uiNode: UITreeNodeWithDisplayRegion
    chatWindow: Optional[ChatWindow]


class OptimalRange(NamedTuple):
    asString: str
    inMeteres: Union[str, int]


class ModuleButtonTooltip:
    uiNode: UITreeNodeWithDisplayRegion
    shortcut: Optional[ShortCut]
    optimalRange: Optional[OptimalRange]


class ParsedText(NamedTuple):
    hour: int
    minute: int


class NeocomClock:
    uiNode: UITreeNodeWithDisplayRegion
    text: str
    parsedText: Union[str, ParsedText]


class Neocom:
    uiNode: UITreeNodeWithDisplayRegion
    iconInventory: Optional[UITreeNodeWithDisplayRegion]
    clock: Optional[NeocomClock]


class AgentConversationWindow:
    uiNode: UITreeNodeWithDisplayRegion


class BookmarkLocationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    submitButton: Optional[UITreeNodeWithDisplayRegion]
    cancelButton: Optional[UITreeNodeWithDisplayRegion]


class ButtonTuples(NamedTuple):
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]


class MessageBox:
    uiNode: UITreeNodeWithDisplayRegion
    buttons: List[ButtonTuples]


class FleetWindow:
    uiNode: UITreeNodeWithDisplayRegion
    fleetMembers: List[UITreeNodeWithDisplayRegion]


class WatchListPanel:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class StandaloneBookmarkWindow:
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class KeyActivationWindow:
    uiNode: UITreeNodeWithDisplayRegion
    activateButton: Optional[UITreeNodeWithDisplayRegion]


class ParsedUserinterface:
    uiTree: UITreeNodeWithDisplayRegion
    contextMenus: List[ContextMenu]
    shipUI: Optional[ShipUI]
    targets: List[Target]
    infoPanelContainer: Optional[InfoPanelContainer]
    overviewWindow: Optional[OverviewWindow]
    selectedItemWindow: Optional[SelectedItemWindow]
    dronesWindow: Optional[DronesWindow]
    fittingWindow: Optional[FittingWindow]
    probeScannerWindow: Optional[ProbeScannerWindow]
    directionalScannerWindow: Optional[DirectionalScannerWindow]
    stationWindow: Optional[StationWindow]
    inventoryWindows: List[InventoryWindow]
    chatWindowStacks: List[ChatWindowStack]
    agentConversationWindows: List[AgentConversationWindow]
    marketOrdersWindow: Optional[MarketOrdersWindow]
    surveyScanWindow: Optional[SurveyScanWindow]
    bookmarkLocationWindow: Optional[BookmarkLocationWindow]
    repairShopWindow: Optional[RepairShopWindow]
    characterSheetWindow: Optional[CharacterSheetWindow]
    fleetWindow: Optional[FleetWindow]
    watchListPanel: Optional[WatchListPanel]
    standaloneBookmarkWindow: Optional[StandaloneBookmarkWindow]
    moduleButtonTooltip: Optional[ModuleButtonTooltip]
    neocom: Optional[Neocom]
    messageBoxes: List[MessageBox]
    layerAbovemain: Optional[UITreeNodeWithDisplayRegion]
    keyActivationWindow: Optional[KeyActivationWindow]


# ### End Alias.


def parseUITreeWithDisplayRegionFromUITree( uiTree: UITreeNode ) -> UITreeNodeWithDisplayRegion:
    pass
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

def parseUserinterfaceFromUITree( uiTree: UITreeNode ) -> ParsedUserinterface:
  pass

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

def asUITreeNodeWithDisplayRegion(selfDisplayRegion: DisplayRegion, totalDisplayRegion: DisplayRegion) -> function:


  def myFunc(node: UITreeNode) -> UITreeNodeWithDisplayRegion:
    pass
  return myFunc

# asUITreeNodeWithDisplayRegion : { selfDisplayRegion : DisplayRegion, totalDisplayRegion : DisplayRegion } -> UITreeNode -> UITreeNodeWithDisplayRegion
# asUITreeNodeWithDisplayRegion { selfDisplayRegion, totalDisplayRegion } uiNode =
#     { uiNode = uiNode
#     , children = uiNode.children |> Maybe.map (List.map (unwrapUITreeNodeChild >> asUITreeNodeWithInheritedOffset { x = totalDisplayRegion.x, y = totalDisplayRegion.y }))
#     , selfDisplayRegion = selfDisplayRegion
#     , totalDisplayRegion = totalDisplayRegion
#     }

def asUITreeNodeWithInheritedOffset(rawNode: NamedTuple(x= int, y= int)) -> function:
  
  def myFunc(node: UITreeNode) -> UITreeNodeWithDisplayRegion:
    pass
  return myFunc

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
  pass
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
  pass

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

def parseContextMenusFromUITreeRoot(uiTreeRoot: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelContainer]:
  pass
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
  pass

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

def parseInfoPanelLocationInfoFromInfoPanelContainer(infoPanelContainerNode:UITreeNodeWithDisplayRegion) -> Optional[InfoPanelLocationInfo]:
  pass
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
  pass
# parseSecurityStatusPercentFromUINodeText : str -> Maybe int
# parseSecurityStatusPercentFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "hint='Security status'"
#         , getSubstrBetweenXmlTagsAfterMarker "hint=\"Security status\"><color="
#         ]
#         >> Maybe.andThen (str.trim >> str.toFloat)
#         >> Maybe.map ((*) 100 >> round)

def parseCurrentSolarSystemFromUINodeText(s: str) -> Optional[str]:
  pass
# parseCurrentSolarSystemFromUINodeText : str -> Maybe str
# parseCurrentSolarSystemFromUINodeText =
#     Maybe.Extra.oneOf
#         [ getSubstrBetweenXmlTagsAfterMarker "alt='Current Solar System'"
#         , getSubstrBetweenXmlTagsAfterMarker "alt=\"Current Solar System\""
#         ]

def parseCurrentStationNameFromInfoPanelLocationInfoLabelText(s: str) -> Optional[str]:
  pass
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText : str -> Maybe str
# parseCurrentStationNameFromInfoPanelLocationInfoLabelText =
#     getSubstrBetweenXmlTagsAfterMarker "alt='Current Station'"
#         >> Maybe.map str.trim

def parseInfoPanelRouteFromInfoPanelContainer(infoPanelContainerNode: UITreeNodeWithDisplayRegion) -> Optional[InfoPanelRoute]:
  pass
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
  pass
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

def parseContextMenu(contextMenuUINOde: UITreeNodeWithDisplayRegion) -> ContextMenu:
  pass
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
  pass
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

def parseShipUIModuleButton( slotNode: UITreeNodeWithDisplayRegion, moduleButtonNode: UITreeNodeWithDisplayRegion) -> ShipUIModuleButton:
  pass
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
  pass
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
#                 |> Maybe.Extra.combine
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

def groupShipUIModulesintoRows( capacitor: ShipUICapacitor ) -> function:
  
  def myFunc(modules: List[ShipUIModuleButton]) -> ModuleRows:
    pass
  return myFunc
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
def parseShipIndication(indicationUINode: UITreeNodeWithDisplayRegion) -> ShipUIIndication:
  pass
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
#             , ( "워프 드라이브 가동", ManeuverWarp )
#             -- Sample `session-2022-05-26T03-13-42-83df2b.zip` shared by Abaddon at https://forum.botlab.org/t/i-want-to-add-korean-support-on-eve-online-bot-what-should-i-do/4370/14
#             , ( "점프 중", ManeuverJump )
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


# parseSquadronsUI : UITreeNodeWithDisplayRegion -> SquadronsUI
# parseSquadronsUI squadronsUINode =
#     { uiNode = squadronsUINode
#     , squadrons =
#         squadronsUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SquadronUI")
#             |> List.map parseSquadronUI
#     }

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

# parseTargetsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List Target
# parseTargetsFromUITreeRoot =
#     listDescendantsWithDisplayRegion
#         >> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "TargetInBar")
#         >> List.map parseTarget

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

# parseOverviewEntryDistanceInMetersFromText : str -> Result str int
# parseOverviewEntryDistanceInMetersFromText distanceDisplayTextBeforeTrim =
#     case distanceDisplayTextBeforeTrim |> str.trim |> str.split " " |> List.reverse of
#         unitText :: reversedNumberTexts ->
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

# parseDistanceUnitInMeters : str -> Maybe int
# parseDistanceUnitInMeters unitText =
#     case str.trim unitText of
#         "m" ->
#             Just 1
#         "km" ->
#             Just 1000
#         _ ->
#             Nothing

# parseSelectedItemWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SelectedItemWindow
# parseSelectedItemWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ActiveItem")
#         |> List.head
#         |> Maybe.map parseSelectedItemWindow

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

# parseInventoryWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List InventoryWindow
# parseInventoryWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (\uiNode -> [ "InventoryPrimary", "ActiveShipCargo" ] |> List.member uiNode.uiNode.pythonObjectTypeName)
#         |> List.map parseInventoryWindow

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

# unwrapInventoryWindowLeftTreeEntryChild : InventoryWindowLeftTreeEntryChild -> InventoryWindowLeftTreeEntry
# unwrapInventoryWindowLeftTreeEntryChild child =
#     case child of
#         InventoryWindowLeftTreeEntryChild unpacked ->
#             unpacked

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
#     case capacityText |> str.replace "m³" "" |> str.split "/" of
#         [ withoutSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = withoutSlash, afterSlashMaybeText = Nothing }
#         [ partBeforeSlash, partAfterSlash ] ->
#             continueAfterSeparatingBySlash { beforeSlashText = partBeforeSlash, afterSlashMaybeText = Just partAfterSlash }
#         _ ->
#             Err ("Unexpected number of components in capacityText '" ++ capacityText ++ "'")

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

# parseChatWindowStacksFromUITreeRoot : UITreeNodeWithDisplayRegion -> List ChatWindowStack
# parseChatWindowStacksFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "ChatWindowStack")
#         |> List.map parseChatWindowStack

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

# parseAgentConversationWindowsFromUITreeRoot : UITreeNodeWithDisplayRegion -> List AgentConversationWindow
# parseAgentConversationWindowsFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "AgentDialogueWindow")
#         |> List.map parseAgentConversationWindow

# parseAgentConversationWindow : UITreeNodeWithDisplayRegion -> AgentConversationWindow
# parseAgentConversationWindow windowUINode =
#     { uiNode = windowUINode
#     }

# parseMarketOrdersWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe MarketOrdersWindow
# parseMarketOrdersWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MarketOrdersWnd")
#         |> List.head
#         |> Maybe.map parseMarketOrdersWindow

# parseMarketOrdersWindow : UITreeNodeWithDisplayRegion -> MarketOrdersWindow
# parseMarketOrdersWindow windowUINode =
#     { uiNode = windowUINode
#     }

# parseFittingWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FittingWindow
# parseFittingWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FittingWindow")
#         |> List.head
#         |> Maybe.map parseFittingWindow

# parseFittingWindow : UITreeNodeWithDisplayRegion -> FittingWindow
# parseFittingWindow windowUINode =
#     { uiNode = windowUINode
#     }

# parseSurveyScanWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe SurveyScanWindow
# parseSurveyScanWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanView")
#         |> List.head
#         |> Maybe.map parseSurveyScanWindow

# parseSurveyScanWindow : UITreeNodeWithDisplayRegion -> SurveyScanWindow
# parseSurveyScanWindow windowUINode =
#     { uiNode = windowUINode
#     , scanEntries =
#         windowUINode
#             |> listDescendantsWithDisplayRegion
#             |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "SurveyScanEntry")
#     }

# parseBookmarkLocationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe BookmarkLocationWindow
# parseBookmarkLocationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "BookmarkLocationWindow")
#         |> List.head
#         |> Maybe.map parseBookmarkLocationWindow

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

# parseRepairShopWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe RepairShopWindow
# parseRepairShopWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "RepairShopWindow")
#         |> List.head
#         |> Maybe.map parseRepairShopWindow

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

# parseCharacterSheetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe CharacterSheetWindow
# parseCharacterSheetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "CharacterSheetWindow")
#         |> List.head
#         |> Maybe.map parseCharacterSheetWindow

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

# parseFleetWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe FleetWindow
# parseFleetWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "FleetWindow")
#         |> List.head
#         |> Maybe.map parseFleetWindow

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

# parseWatchListPanelFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe WatchListPanel
# parseWatchListPanelFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "WatchListPanel")
#         |> List.head
#         |> Maybe.map parseWatchListPanel

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

# parseStandaloneBookmarkWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe StandaloneBookmarkWindow
# parseStandaloneBookmarkWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "StandaloneBookmarkWnd")
#         |> List.head
#         |> Maybe.map parseStandaloneBookmarkWindow

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

# parseKeyActivationWindowFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe KeyActivationWindow
# parseKeyActivationWindowFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "KeyActivationWindow")
#         |> List.head
#         |> Maybe.map parseKeyActivationWindow

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

# parseMessageBoxesFromUITreeRoot : UITreeNodeWithDisplayRegion -> List MessageBox
# parseMessageBoxesFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> .pythonObjectTypeName >> (==) "MessageBox")
#         |> List.map parseMessageBox

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

# parseLayerAbovemainFromUITreeRoot : UITreeNodeWithDisplayRegion -> Maybe UITreeNodeWithDisplayRegion
# parseLayerAbovemainFromUITreeRoot uiTreeRoot =
#     uiTreeRoot
#         |> listDescendantsWithDisplayRegion
#         |> List.filter (.uiNode >> getNameFromDictEntries >> (==) (Just "l_abovemain"))
#         |> List.head

# getSubstrBetweenXmlTagsAfterMarker : str -> str -> Maybe str
# getSubstrBetweenXmlTagsAfterMarker marker =
#     str.split marker
#         >> List.drop 1
#         >> List.head
#         >> Maybe.andThen (str.split ">" >> List.drop 1 >> List.head)
#         >> Maybe.andThen (str.split "<" >> List.head)

# parseNumberTruncatingAfterOptionalDecimalSeparator : str -> Result str int
# parseNumberTruncatingAfterOptionalDecimalSeparator numberDisplayText =
#     let
#         expectedSeparators =
#             [ ",", ".", "’", " ", "\u{00A0}", "\u{202F}" ]
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

# centerFromDisplayRegion : DisplayRegion -> Location2d
# centerFromDisplayRegion region =
#     { x = region.x + region.width // 2, y = region.y + region.height // 2 }

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

# getAllContainedDisplayTexts : UITreeNode -> List str
# getAllContainedDisplayTexts uiNode =
#     uiNode
#         :: (uiNode |> listDescendantsInUITreeNode)
#         |> List.filterMap getDisplayText

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

# getNameFromDictEntries : UITreeNode -> Maybe str
# getNameFromDictEntries =
#     getstrPropertyFromDictEntries "_name"

# getHintTextFromDictEntries : UITreeNode -> Maybe str
# getHintTextFromDictEntries =
#     getstrPropertyFromDictEntries "_hint"

# getTexturePathFromDictEntries : UITreeNode -> Maybe str
# getTexturePathFromDictEntries =
#     getstrPropertyFromDictEntries "texturePath"

# getstrPropertyFromDictEntries : str -> UITreeNode -> Maybe str
# getstrPropertyFromDictEntries dictEntryKey uiNode =
#     uiNode.dictEntriesOfinterest
#         |> Dict.get dictEntryKey
#         |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.str >> Result.toMaybe)

# getColorPercentFromDictEntries : UITreeNode -> Maybe ColorComponents
# getColorPercentFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_color"
#         >> Maybe.andThen (Json.Decode.decodeValue jsonDecodeColorPercent >> Result.toMaybe)

# jsonDecodeColorPercent : Json.Decode.Decoder ColorComponents
# jsonDecodeColorPercent =
#     Json.Decode.map4 ColorComponents
#         (Json.Decode.field "aPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "rPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "gPercent" jsonDecodeintFromintOrstr)
#         (Json.Decode.field "bPercent" jsonDecodeintFromintOrstr)

# getRotationFloatFromDictEntries : UITreeNode -> Maybe Float
# getRotationFloatFromDictEntries =
#     .dictEntriesOfinterest
#         >> Dict.get "_rotation"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)

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

# areaFromDisplayRegion : DisplayRegion -> Maybe int
# areaFromDisplayRegion region =
#     if region.width < 0 || region.height < 0 then
#         Nothing
#     else
#         Just (region.width * region.height)

# getVerticalOffsetFromParent : UITreeNode -> Maybe int
# getVerticalOffsetFromParent =
#     .dictEntriesOfinterest
#         >> Dict.get "_displayY"
#         >> Maybe.andThen (Json.Decode.decodeValue Json.Decode.float >> Result.toMaybe)
#         >> Maybe.map round

# getMostPopulousDescendantMatchingPredicate : (UITreeNode -> bool) -> UITreeNode -> Maybe UITreeNode
# getMostPopulousDescendantMatchingPredicate predicate parent =
#     listDescendantsInUITreeNode parent
#         |> List.filter predicate
#         |> List.sortBy countDescendantsInUITreeNode
#         |> List.reverse
#         |> List.head

# listDescendantsWithDisplayRegion : UITreeNodeWithDisplayRegion -> List UITreeNodeWithDisplayRegion
# listDescendantsWithDisplayRegion parent =
#     parent
#         |> listChildrenWithDisplayRegion
#         |> List.concatMap (\child -> child :: listDescendantsWithDisplayRegion child)

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