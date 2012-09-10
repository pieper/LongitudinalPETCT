# slicer imports
from __main__ import vtk, slicer, tcl, qt

# python includes
import sys
import time

class SlicerLongPETCTModuleViewHelper( object ):
  '''
  classdocs
  '''

  # TODO: add a capability to control the level of messages
  @staticmethod
  def Info( message ):
    print("[Reporting " + time.strftime( "%m/%d/%Y %H:%M:%S" ) + "]: INFO: " + str( message ))
    sys.stdout.flush()


  @staticmethod
  def SetBgFgLblVolumes(bgID, fgID = None, lblID = None, propagate = True):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    selectionNode.SetReferenceActiveVolumeID(bgID)
    selectionNode.SetReferenceSecondaryVolumeID(fgID)
    selectionNode.SetReferenceActiveLabelVolumeID(lblID)
    
    if fgID:
      compositeNodes = slicer.util.getNodes('vtkMRMLSliceCompositeNode*')
      for compositeNode in compositeNodes.values():
        compositeNode.SetForegroundOpacity(0.6)
    
    if propagate:
      appLogic.PropagateVolumeSelection()


  @staticmethod
  def SetForegroundWindowLevel(window, level):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    fgVolumeNodeID = selectionNode.GetSecondaryVolumeID()
    print fgVolumeNodeID
    fgVolumeNode = slicer.mrmlScene.GetNodeByID(fgVolumeNodeID)
    
    if fgVolumeNode:
      fgDisplayNode = fgVolumeNode.GetScalarVolumeDisplayNode()
      if fgDisplayNode:
        fgDisplayNode.SetWindow(window)
        fgDisplayNode.SetLevel(level)
        
  @staticmethod
  def SetBackgroundWindowLevel(window, level):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    bgVolumeNodeID = selectionNode.GetActiveVolumeID()
    bgVolumeNode = slicer.mrmlScene.GetNodeByID(bgVolumeNodeID)
    
    if bgVolumeNode:
      bgDisplayNode = bgVolumeNode.GetScalarVolumeDisplayNode()
      if bgDisplayNode:
        bgDisplayNode.SetWindow(window)
        bgDisplayNode.SetLevel(level)

  @staticmethod
  def SetLabelVolume(lblID):
    appLogic = slicer.app.applicationLogic()
    selectionNode = appLogic.GetSelectionNode()
    selectionNode.SetReferenceActiveLabelVolumeID(label)
    appLogic.PropagateVolumeSelection()

  @staticmethod
  def getEditorParameterNode():
    """Get the Editor parameter node - a singleton in the scene"""
    node = None
    size =  slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLScriptedModuleNode")
    for i in xrange(size):
      n  = slicer.mrmlScene.GetNthNodeByClass( i, "vtkMRMLScriptedModuleNode" )
      if n.GetModuleName() == "Editor":
        node = n

    if not node:
      node = slicer.vtkMRMLScriptedModuleNode()
      node.SetSingletonTag( "Editor" )
      node.SetModuleName( "Editor" )
      node.SetParameter( "label", "1" )
      slicer.mrmlScene.AddNode(node)
    return node
  
  
  @staticmethod 
  def getSliceNodesCrossingPositionRAS():
    red = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    yellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    green = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    
    crossing = [0,0,0]
    
    orientation = "Sagittal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        crossing[0] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        crossing[0] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        crossing[0] = green.GetSliceOffset() 
    
    orientation = "Coronal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        crossing[1] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        crossing[1] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        crossing[1] = green.GetSliceOffset() 
        
    orientation = "Axial"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        crossing[2] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        crossing[2] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        crossing[2] = green.GetSliceOffset()   
        
    return crossing
  
  
  @staticmethod 
  def setSliceNodesCrossingPositionRAS(crossingRAS = [0.,0.,0.]):
    red = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    yellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    green = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    
    orientation = "Sagittal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        red.SetSliceOffset(crossingRAS[0])
      if yellow.GetOrientationString() == orientation:
        yellow.SetSliceOffset(crossingRAS[0])
      if green.GetOrientationString() == orientation:
        green.SetSliceOffset(crossingRAS[0])
    
    orientation = "Coronal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        red.SetSliceOffset(crossingRAS[1])
      if yellow.GetOrientationString() == orientation:
        yellow.SetSliceOffset(crossingRAS[1])
      if green.GetOrientationString() == orientation:
        green.SetSliceOffset(crossingRAS[1])
        
    orientation = "Axial"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        red.SetSliceOffset(crossingRAS[2])
      if yellow.GetOrientationString() == orientation:
        yellow.SetSliceOffset(crossingRAS[2])
      if green.GetOrientationString() == orientation:
        green.SetSliceOffset(crossingRAS[2])
        
        
  
  @staticmethod
  def centerROIonSliceNodesOffset(roi, centeringTransform):
    red = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    yellow = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    green = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    roiXYZ = [0,0,0]
    
    orientation = "Sagittal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        roiXYZ[0] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        roiXYZ[0] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        roiXYZ[0] = green.GetSliceOffset() 
    
    orientation = "Coronal"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        roiXYZ[1] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        roiXYZ[1] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        roiXYZ[1] = green.GetSliceOffset() 
        
    orientation = "Axial"
    if (red.GetOrientationString() == orientation) | (yellow.GetOrientationString() == orientation) | (green.GetOrientationString() == orientation):
      if red.GetOrientationString() == orientation:
        roiXYZ[2] = red.GetSliceOffset()
      elif yellow.GetOrientationString() == orientation:
        roiXYZ[2] = yellow.GetSliceOffset() 
      elif green.GetOrientationString() == orientation:
        roiXYZ[2] = green.GetSliceOffset()   
    
    if centerTransform:
      roi.SetAndObserveTransformNodeID(centerTransform.GetID())   
      centerTransformMatrix = centerTransform.GetMatrixTransformToParent()
      roi.SetXYZ(roiXYZ[0]-centerTransformMatrix.GetElement(0,3),roiXYZ[1]-centerTransformMatrix.GetElement(1,3),roiXYZ[2]-centerTransformMatrix.GetElement(2,3))  
    else:
      roi.SetXYZ(roiXYZ)