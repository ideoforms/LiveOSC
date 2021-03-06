"""
# Copyright (C) 2007 Rob King (rob@re-mu.org)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Rob King <rob@e-mu.org> or visit http://www.e-mu.org

This file contains all the current Live OSC callbacks. 

"""
import Live
import RemixNet
import OSC
import LiveUtils
import sys
import re
import time

from Logger import log


class LiveOSCCallbacks:
    def __init__(self, c_instance, oscEndpoint):
        self.oscEndpoint = oscEndpoint
        self.callbackManager = oscEndpoint.callbackManager

        self.c_instance = c_instance

        self.callbackManager.add("/live/tempo", self.tempoCB)
        self.callbackManager.add("/live/time", self.timeCB)
        self.callbackManager.add("/live/next/cue", self.nextCueCB)
        self.callbackManager.add("/live/prev/cue", self.prevCueCB)
        self.callbackManager.add("/live/play", self.playCB)
        self.callbackManager.add("/live/play/continue", self.playContinueCB)
        self.callbackManager.add("/live/play/selection", self.playSelectionCB)
        self.callbackManager.add("/live/play/clip", self.playClipCB)
        self.callbackManager.add("/live/play/scene", self.playSceneCB)
        self.callbackManager.add("/live/scene/create", self.createSceneCB)
        self.callbackManager.add("/live/stop", self.stopCB)
        self.callbackManager.add("/live/stop/clip", self.stopClipCB)
        self.callbackManager.add("/live/stop/track", self.stopTrackCB)
        self.callbackManager.add("/live/scenes", self.scenesCB)
        self.callbackManager.add("/live/tracks", self.tracksCB)
        self.callbackManager.add("/live/name/scene", self.nameSceneCB)
        self.callbackManager.add("/live/scene", self.sceneCB)
        self.callbackManager.add("/live/name/sceneblock", self.nameSceneBlockCB)
        self.callbackManager.add("/live/name/track", self.nameTrackCB)
        self.callbackManager.add("/live/name/trackblock", self.nameTrackBlockCB)
        self.callbackManager.add("/live/name/clip", self.nameClipCB)
        self.callbackManager.add("/live/name/clipblock", self.nameClipBlockCB)    
        self.callbackManager.add("/live/arm", self.armTrackCB)
        self.callbackManager.add("/live/mute", self.muteTrackCB)
        self.callbackManager.add("/live/solo", self.soloTrackCB)
        self.callbackManager.add("/live/volume", self.volumeCB)
        self.callbackManager.add("/live/pan", self.panCB)
        self.callbackManager.add("/live/send", self.sendCB)
        self.callbackManager.add("/live/pitch", self.pitchCB)
        self.callbackManager.add("/live/track/jump", self.trackJump)
        self.callbackManager.add("/live/track/info", self.trackInfoCB)
        self.callbackManager.add("/live/undo", self.undoCB)
        self.callbackManager.add("/live/redo", self.redoCB)
        self.callbackManager.add("/live/play/clipslot", self.playClipSlotCB)
        
        self.callbackManager.add("/live/scene/view", self.viewSceneCB)
        
        self.callbackManager.add("/live/track/view", self.viewTrackCB)
        self.callbackManager.add("/live/return/view", self.viewTrackCB)
        self.callbackManager.add("/live/master/view", self.mviewTrackCB)
        
        self.callbackManager.add("/live/track/device/view", self.viewDeviceCB)
        self.callbackManager.add("/live/return/device/view", self.viewDeviceCB)
        self.callbackManager.add("/live/master/device/view", self.mviewDeviceCB)        
        
        self.callbackManager.add("/live/clip/view", self.viewClipCB)
        
        self.callbackManager.add("/live/detail/view", self.detailViewCB)
        
        self.callbackManager.add("/live/overdub", self.overdubCB)
        self.callbackManager.add("/live/state", self.stateCB)
        self.callbackManager.add("/live/clip/info", self.clipInfoCB)
        
        self.callbackManager.add("/live/return/mute", self.muteTrackCB)
        self.callbackManager.add("/live/return/solo", self.soloTrackCB)
        self.callbackManager.add("/live/return/volume", self.volumeCB)
        self.callbackManager.add("/live/return/pan", self.panCB)
        self.callbackManager.add("/live/return/send", self.sendCB)        

        self.callbackManager.add("/live/master/volume", self.volumeCB)
        self.callbackManager.add("/live/master/pan", self.panCB)
        
        self.callbackManager.add("/live/devicelist", self.devicelistCB)
        self.callbackManager.add("/live/return/devicelist", self.devicelistCB)
        self.callbackManager.add("/live/master/devicelist", self.mdevicelistCB)

        self.callbackManager.add("/live/device/range", self.devicerangeCB)
        self.callbackManager.add("/live/return/device/range", self.devicerangeCB)
        self.callbackManager.add("/live/master/device/range", self.mdevicerangeCB)
        
        self.callbackManager.add("/live/device", self.deviceCB)
        self.callbackManager.add("/live/return/device", self.deviceCB)
        self.callbackManager.add("/live/master/device", self.mdeviceCB)
        
        self.callbackManager.add("/live/clip/loopstate", self.loopStateCB)
        self.callbackManager.add("/live/clip/loopstart", self.loopStartCB)
        self.callbackManager.add("/live/clip/loopend", self.loopEndCB)
        
        self.callbackManager.add("/live/clip/loopstate_id", self.loopStateCB)
        self.callbackManager.add("/live/clip/loopstart_id", self.loopStartCB)
        self.callbackManager.add("/live/clip/loopend_id", self.loopEndCB)
        
        self.callbackManager.add("/live/clip/warping", self.warpingCB)
        
        self.callbackManager.add("/live/clip/signature", self.sigCB)

        self.callbackManager.add("/live/clip/add_note", self.addNoteCB)
        self.callbackManager.add("/live/clip/notes", self.getNotesCB)
        self.callbackManager.add("/live/clip/create", self.createClipCB)
        self.callbackManager.add("/live/clip/delete", self.deleteClipCB)

        self.callbackManager.add("/live/clip/mute", self.muteClipCB)

        self.callbackManager.add("/live/master/crossfader", self.crossfaderCB)
        self.callbackManager.add("/live/track/crossfader", self.trackxfaderCB)
        self.callbackManager.add("/live/return/crossfader", self.trackxfaderCB)

        self.callbackManager.add("/live/quantization", self.quantizationCB)

        self.callbackManager.add("/live/selection", self.selectionCB)

        self.callbackManager.add("/live/deactivate", self.deactivateCB)
        self.callbackManager.add("/live/clear_inactive", self.clearInactiveCB)
        self.callbackManager.add("/live/filter_clips", self.filterClipsCB)
        self.callbackManager.add("/live/unfilter_group", self.unfilterGroupCB)
        self.callbackManager.add("/live/distribute_groups", self.distributeGroupsCB)
        self.callbackManager.add("/live/play/group_scene", self.playGroupSceneCB)

        self.clip_notes_cache = {}

    def sigCB(self, msg, source):
        """ Called when a /live/clip/signature message is recieved
        """
        track = msg[2]
        clip = msg[3]
        c = LiveUtils.getSong().tracks[track].clip_slots[clip].clip
        
        if len(msg) == 4:
            self.oscEndpoint.send("/live/clip/signature", (track, clip, c.signature_numerator, c.signature_denominator))
            
        if len(msg) == 6:
            self.oscEndpoint.send("/live/clip/signature", 1)
            c.signature_denominator = msg[5]
            c.signature_numerator = msg[4]

    def warpingCB(self, msg, source):
        """ Called when a /live/clip/warping message is recieved
        """
        track = msg[2]
        clip = msg[3]
        
        
        if len(msg) == 4:
            state = LiveUtils.getSong().tracks[track].clip_slots[clip].clip.warping
            self.oscEndpoint.send("/live/clip/warping", (track, clip, int(state)))
        
        elif len(msg) == 5:
            LiveUtils.getSong().tracks[track].clip_slots[clip].clip.warping = msg[4]

    def selectionCB(self, msg, source):
        """ Called when a /live/selection message is received
        """
        if len(msg) == 6:
            self.c_instance.set_session_highlight(msg[2], msg[3], msg[4], msg[5], 0)

    def trackxfaderCB(self, msg, source):
        """ Called when a /live/track/crossfader or /live/return/crossfader message is received
        """
        ty = msg[0] == '/live/return/crossfader' and 1 or 0
    
        if len(msg) == 3:
            track = msg[2]
        
            if ty == 1:
                assign = LiveUtils.getSong().return_tracks[track].mixer_device.crossfade_assign
                name   = LiveUtils.getSong().return_tracks[track].mixer_device.crossfade_assignments.values[assign]
            
                self.oscEndpoint.send("/live/return/crossfader", (track, str(assign), str(name)))
            else:
                assign = LiveUtils.getSong().tracks[track].mixer_device.crossfade_assign
                name   = LiveUtils.getSong().tracks[track].mixer_device.crossfade_assignments.values[assign]
            
                self.oscEndpoint.send("/live/track/crossfader", (track, str(assign), str(name)))

            
        elif len(msg) == 4:
            track = msg[2]
            assign = msg[3]
            
            if ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.crossfade_assign = assign
            else:
                LiveUtils.getSong().tracks[track].mixer_device.crossfade_assign = assign

    def tempoCB(self, msg, source):
        """Called when a /live/tempo message is received.

        Messages:
        /live/tempo                 Request current tempo, replies with /live/tempo (float tempo)
        /live/tempo (float tempo)   Set the tempo, replies with /live/tempo (float tempo)
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscEndpoint.send("/live/tempo", LiveUtils.getTempo())
        
        elif len(msg) == 3:
            tempo = msg[2]
            LiveUtils.setTempo(tempo)
        
    def timeCB(self, msg, source):
        """Called when a /live/time message is received.

        Messages:
        /live/time                 Request current song time, replies with /live/time (float time)
        /live/time (float time)    Set the time , replies with /live/time (float time)
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscEndpoint.send("/live/time", float(LiveUtils.currentTime()))

        elif len(msg) == 3:
            time = msg[2]
            LiveUtils.currentTime(time)

    def nextCueCB(self, msg, source):
        """Called when a /live/next/cue message is received.

        Messages:
        /live/next/cue              Jumps to the next cue point
        """
        LiveUtils.jumpToNextCue()
        
    def prevCueCB(self, msg, source):
        """Called when a /live/prev/cue message is received.

        Messages:
        /live/prev/cue              Jumps to the previous cue point
        """
        LiveUtils.jumpToPrevCue()
        
    def playCB(self, msg, source):
        """Called when a /live/play message is received.

        Messages:
        /live/play              Starts the song playing
        """
        LiveUtils.play()
        
    def playContinueCB(self, msg, source):
        """Called when a /live/play/continue message is received.

        Messages:
        /live/play/continue     Continues playing the song from the current point
        """
        LiveUtils.continuePlaying()
        
    def playSelectionCB(self, msg, source):
        """Called when a /live/play/selection message is received.

        Messages:
        /live/play/selection    Plays the current selection
        """
        LiveUtils.playSelection()
        
    def playClipCB(self, msg, source):
        """Called when a /live/play/clip message is received.

        Messages:
        /live/play/clip     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            track = msg[2]
            clip = msg[3]
            LiveUtils.launchClip(track, clip)
            
    def playSceneCB(self, msg, source):
        """Called when a /live/play/scene message is received.

        Messages:
        /live/play/scene    (int scene)     Launches scene number scene
        """
        if len(msg) == 3:
            scene = msg[2]
            LiveUtils.launchScene(scene)
    
    def createSceneCB(self, msg, source):
        """Called when a /live/scene/create message is received.

        Messages:
        /live/scene/create    (int scene)     create a scene at the index
        """
        if len(msg) == 3:
            scene = msg[2]
            LiveUtils.createScene(scene)
            
            
    
    def stopCB(self, msg, source):
        """Called when a /live/stop message is received.

        Messages:
        /live/stop              Stops playing the song
        """
        LiveUtils.stop()
        
    def stopClipCB(self, msg, source):
        """Called when a /live/stop/clip message is received.

        Messages:
        /live/stop/clip     (int track, int clip)   Stops clip number clip in track number track
        """
        if len(msg) == 4:
            track = msg[2]
            clip = msg[3]
            LiveUtils.stopClip(track, clip)

    def stopTrackCB(self, msg, source):
        """Called when a /live/stop/track message is received.

        Messages:
        /live/stop/track     (int track, int clip)   Stops track number track
        """
        if len(msg) == 3:
            track = msg[2]
            LiveUtils.stopTrack(track)

    def scenesCB(self, msg, source):
        """Called when a /live/scenes message is received.

        Messages:
        /live/scenes        no argument or 'query'  Returns the total number of scenes

        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            sceneTotal = len(LiveUtils.getScenes())
            self.oscEndpoint.send("/live/scenes", (sceneTotal))
            return

    def sceneCB(self, msg, source):
        """Called when a /live/scene message is received.
        
        Messages:
        /live/scene         no argument or 'query'  Returns the currently playing scene number
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            selected_scene = LiveUtils.getSong().view.selected_scene
            scenes = LiveUtils.getScenes()
            index = 0
            selected_index = 0
            for scene in scenes:
                index = index + 1        
                if scene == selected_scene:
                    selected_index = index
                    
            self.oscEndpoint.send("/live/scene", (selected_index))
            
        elif len(msg) == 3:
            scene = msg[2]
            LiveUtils.getSong().view.selected_scene = LiveUtils.getSong().scenes[scene]

    def tracksCB(self, msg, source):
        """Called when a /live/tracks message is received.

        Messages:
        /live/tracks       no argument or 'query'  Returns the total number of scenes

        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackTotal = len(LiveUtils.getTracks())
            self.oscEndpoint.send("/live/tracks", (trackTotal))
            return


    def nameSceneCB(self, msg, source):
        """Called when a /live/name/scene message is received.

        Messages:
        /live/name/scene                            Returns a a series of all the scene names in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene)             Returns a single scene's name in the form /live/name/scene (int scene, string name)
        /live/name/scene    (int scene, string name)Sets scene number scene's name to name

        """        
        #Requesting all scene names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            bundle = OSC.OSCBundle()
            sceneNumber = 0
            for scene in LiveUtils.getScenes():
                bundle.append("/live/name/scene", (sceneNumber, str(scene.name)))
                sceneNumber = sceneNumber + 1
            self.oscEndpoint.sendMessage(bundle)
            return
        #Requesting a single scene name
        if len(msg) == 3:
            sceneNumber = msg[2]
            self.oscEndpoint.send("/live/name/scene", (sceneNumber, str(LiveUtils.getScene(sceneNumber).name)))
            return
        #renaming a scene
        if len(msg) == 4:
            sceneNumber = msg[2]
            name = msg[3]
            LiveUtils.getScene(sceneNumber).name = name

    def nameSceneBlockCB(self, msg, source):
        """Called when a /live/name/sceneblock message is received.

        /live/name/clipblock    (int offset, int blocksize) Returns a list of blocksize scene names starting at offset
        """
        if len(msg) == 4:
            block = []
            sceneOffset = msg[2]
            blocksize = msg[3]
            for scene in range(0, blocksize):
                block.extend([str(LiveUtils.getScene(sceneOffset+scene).name)])                            
            self.oscEndpoint.send("/live/name/sceneblock", block)
            
            
    def nameTrackCB(self, msg, source):
        """Called when a /live/name/track message is received.

        Messages:
        /live/name/track                            Returns a a series of all the track names in the form /live/name/track (int track, string name)
        /live/name/track    (int track)             Returns a single track's name in the form /live/name/track (int track, string name)
        /live/name/track    (int track, string name)Sets track number track's name to name

        """
        #Requesting all track names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackNumber = 0
            bundle = OSC.OSCBundle()
            for track in LiveUtils.getTracks():
                bundle.append("/live/name/track", (trackNumber, str(track.name)))
                trackNumber = trackNumber + 1
            self.oscEndpoint.sendMessage(bundle)
            return
        #Requesting a single track name
        if len(msg) == 3:
            trackNumber = msg[2]
            self.oscEndpoint.send("/live/name/track", (trackNumber, str(LiveUtils.getTrack(trackNumber).name)))
            return
        #renaming a track
        if len(msg) == 4:
            trackNumber = msg[2]
            name = msg[3]
            LiveUtils.getTrack(trackNumber).name = name

    def nameTrackBlockCB(self, msg, source):
        """Called when a /live/name/trackblock message is received.

        /live/name/trackblock    (int offset, int blocksize) Returns a list of blocksize track names starting at offset
        """
        if len(msg) == 4:
            block = []
            trackOffset = msg[2]
            blocksize = msg[3]
            for track in range(0, blocksize):
                block.extend([str(LiveUtils.getTrack(trackOffset+track).name)])                            
            self.oscEndpoint.send("/live/name/trackblock", block)

    def nameClipBlockCB(self, msg, source):
        """Called when a /live/name/clipblock message is received.

        /live/name/clipblock    (int track, int clip, blocksize x/tracks, blocksize y/clipslots) Returns a list of clip names for a block of clips (int blockX, int blockY, clipname)

        """
        #Requesting a block of clip names X1 Y1 X2 Y2 where X1,Y1 is the first clip (track, clip) of the block, X2 the number of tracks to cover and Y2 the number of scenes
        
        if len(msg) == 6:
            block = []
            trackOffset = msg[2]
            clipOffset = msg[3]
            blocksizeX = msg[4]
            blocksizeY = msg[5]
            for clip in range(0, blocksizeY):
                for track in range(0, blocksizeX):
                        trackNumber = trackOffset+track
                        clipNumber = clipOffset+clip
                        if LiveUtils.getClip(trackNumber, clipNumber) != None:
                            block.extend([str(LiveUtils.getClip(trackNumber, clipNumber).name)])
                        else:
                            block.extend([""])
                            
            self.oscEndpoint.send("/live/name/clipblock", block)



    def nameClipCB(self, msg, source):
        """Called when a /live/name/clip message is received.

        Messages:
        /live/name/clip                                      Returns a a series of all the clip names in the form /live/name/clip (int track, int clip, string name)
        /live/name/clip    (int track, int clip)             Returns a single clip's name in the form /live/name/clip (int clip, string name)
        /live/name/clip    (int track, int clip, string name)Sets clip number clip in track number track's name to name

        """
        #Requesting all clip names
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            trackNumber = 0
            clipNumber = 0
            for track in LiveUtils.getTracks():
                bundle = OSC.OSCBundle()
                for clipSlot in track.clip_slots:
                    if clipSlot.clip != None:
                        bundle.append("/live/name/clip", (trackNumber, clipNumber, str(clipSlot.clip.name), clipSlot.clip.color))
                    clipNumber = clipNumber + 1
                self.oscEndpoint.sendMessage(bundle)
                clipNumber = 0
                trackNumber = trackNumber + 1
            return
        #Requesting a single clip name
        if len(msg) == 4:
            trackNumber = msg[2]
            clipNumber = msg[3]
            self.oscEndpoint.send("/live/name/clip", (trackNumber, clipNumber, str(LiveUtils.getClip(trackNumber, clipNumber).name), LiveUtils.getClip(trackNumber, clipNumber).color))
            return
        #renaming a clip
        if len(msg) >= 5:
            trackNumber = msg[2]
            clipNumber = msg[3]
            name = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).name = name

        if len(msg) >= 6:
            trackNumber = msg[2]
            clipNumber = msg[3]
            color = msg[5]
            LiveUtils.getClip(trackNumber, clipNumber).color = color

    def addNoteCB(self, msg, source):
        """Called when a /live/clip/add_note message is received

        Messages:
        /live/clip/add_note (int pitch) (double time) (double duration) (int velocity) (bool muted)    Add the given note to the clip
        """
        trackNumber = msg[2]
        clipNumber = msg[3]
        pitch = msg[4]
        time = msg[5]
        duration = msg[6]
        velocity = msg[7]
        muted = msg[8]
        LiveUtils.getClip(trackNumber, clipNumber).deselect_all_notes()

        notes = ((pitch, time, duration, velocity, muted),)
        LiveUtils.getClip(trackNumber, clipNumber).replace_selected_notes(notes)
        self.oscEndpoint.send('/live/clip/note', (trackNumber, clipNumber, pitch, time, duration, velocity, muted))

    def getNotesCB(self, msg, source):
        """Called when a /live/clip/notes message is received

        Messages:
        /live/clip/notes    Return all notes in the clip in /live/clip/note messages.  Each note is sent in the format
                            (int trackNumber) (int clipNumber) (int pitch) (double time) (double duration) (int velocity) (int muted)
        """
        trackNumber = msg[2]
        clipNumber = msg[3]
        LiveUtils.getClip(trackNumber, clipNumber).select_all_notes()
        bundle = OSC.OSCBundle()
        for note in LiveUtils.getClip(trackNumber, clipNumber).get_selected_notes():
            pitch = note[0]
            time = note[1]
            duration = note[2]
            velocity = note[3]
            muted = 0
            if note[4]:
                muted = 1
            bundle.append('/live/clip/note', (trackNumber, clipNumber, pitch, time, duration, velocity, muted))
        self.oscEndpoint.sendMessage(bundle)

    def createClipCB(self, msg, source):
        """
        Messages:
        /live/clip/create (int track, int slot, float length)
        Create a clip in [track, slot], length [length] beats
        """
        clipSlots = LiveUtils.getClipSlots()
        track_index = msg[2]
        clipslot_index = msg[3]
        length = msg[4]

        track = LiveUtils.getTrack(track_index)
        clipslot = track.clip_slots[clipslot_index]
        clipslot.create_clip(length)
    
    def deleteClipCB(self, msg, source):
        """
        Messages:
        /live/clip/delete (int track, int slot)
        Delete clip at [track, slot]
        """
        clipSlots = LiveUtils.getClipSlots()
        track_index = msg[2]
        clipslot_index = msg[3]

        track = LiveUtils.getTrack(track_index)
        clipslot = track.clip_slots[clipslot_index]
        clipslot.delete_clip()
    
    def armTrackCB(self, msg, source):
        """Called when a /live/arm message is received.

        Messages:
        /live/arm     (int track)   (int armed/disarmed)     Arms track number track
        """
        track = msg[2]
        
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.armTrack(track)
            else:
                LiveUtils.disarmTrack(track)
        # Return arm status        
        elif len(msg) == 3:
            status = LiveUtils.getTrack(track).arm
            self.oscEndpoint.send("/live/arm", (track, int(status)))     
            
    def muteTrackCB(self, msg, source):
        """Called when a /live/mute message is received.

        Messages:
        /live/mute     (int track)   Mutes track number track
        """
        ty = msg[0] == '/live/return/mute' and 1 or 0
        track = msg[2]
            
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.muteTrack(track, ty)
            else:
                LiveUtils.unmuteTrack(track, ty)
                
        elif len(msg) == 3:
            if ty == 1:
                status = LiveUtils.getSong().return_tracks[track].mute
                self.oscEndpoint.send("/live/return/mute", (track, int(status)))
                
            else:
                status = LiveUtils.getTrack(track).mute
                self.oscEndpoint.send("/live/mute", (track, int(status)))

    def deactivateCB(self, msg, source):
        for track in LiveUtils.getTracks():
            for slot in track.clip_slots:
                if slot.clip != None:
                    slot.clip.muted = True

    def clearInactiveCB(self, msg, source):
        log("clearing inactive")
        for track in LiveUtils.getTracks():
            for slot in track.clip_slots:
                if slot.clip != None and slot.clip.muted:
                    slot.delete_clip()

    def nameToMIDI(self, name):
        """ Maps a MIDI note name (D3, C#6) to a value.
        Assumes that middle C is C4. """
        note_names = [
            [ "C" ],
            [ "C#", "Db" ],
            [ "D" ],
            [ "D#", "Eb" ],
            [ "E" ],
            [ "F" ],
            [ "F#", "Gb" ],
            [ "G" ],
            [ "G#", "Ab" ],
            [ "A" ],
            [ "A#", "Bb" ],
            [ "B" ]
        ]

        for index, names in enumerate(note_names):
            if name in names:
                return index
        return None

    def unfilterGroupCB(self, msg, source):
        track_index = msg[2]
        tracks = LiveUtils.getTracks()
        group = tracks[track_index]
        if group.is_foldable:
            for track in tracks[track_index+1:]:
                if track.is_foldable:
                    break
                else:
                    for clipslot in track.clip_slots:
                        if clipslot.clip is not None:
                            clipslot.clip.muted = False
        else:
            log("unfilterGroupCB: Target is not a group (ID %d)" % track_index)
                
    def filterClipsCB(self, msg, source):
        def bipolar_diverge(maximum):
            """ returns [0, 1, -1, ...., maximum, -maximum ] """
            sequence = list(sum(list(zip(list(range(maximum + 1)), list(range(0, -maximum - 1, -1)))), ()))
            sequence.pop(0)
            return sequence

        def filter_tone_row(source, target, bend_limit = 7):
            """ filters the notes in <source> by the permitted notes in <target>.
            returns a tuple (<bool> acceptable, <int> pitch_bend) """
            bends = bipolar_diverge(bend_limit)
            for bend in bends:
                if all(((note + bend) % 12) in target for note in source):
                    return (True, bend)
            return (False, 0)

        if not self.clip_notes_cache:
            log("no cache found, creating")
            self._filterClipsMakeCache()

        try:
            t0 = time.time()
            note_names = msg[2:]
            log("filtering clips according to %s" % note_names)
            target = tuple(self.nameToMIDI(note) for note in note_names)

            clip_states = {}
            if target in self.clip_tone_row_cache:
                log(" - found cached")
                clip_states = self.clip_tone_row_cache[target]
            else:
                log(" - not found in cache, calculating")
                for track_index, track in enumerate(LiveUtils.getTracks()):
                    for clip_index, slot in enumerate(track.clip_slots):
                        if slot.clip != None:
                            notes = self.clip_notes_cache[track_index][clip_index]
                            # log(" - found notes: %s" % notes)

                            if notes:
                                # don't transpose for now
                                acceptable, bend = filter_tone_row(notes, target, 0)
                                clip_states[slot.clip] = acceptable
                self.clip_tone_row_cache[target] = clip_states

            for clip, acceptable in clip_states.items():
                clip.muted = not acceptable
        except Exception, e:
            log("filtering failed (%s); rebuilding cache" % e)
            self._filterClipsMakeCache()

        log("filtered clips (took %.3fs)" % (time.time() - t0))

    def _filterClipsMakeCache(self, msg = None, source = None):
        self.clip_notes_cache = {}
        self.clip_tone_row_cache = {}
        log("making clip filter cache")
        t0 = time.time()
        try:
            for track_index, track in enumerate(LiveUtils.getTracks()):
                self.clip_notes_cache[track_index] = {}
                for clip_index, slot in enumerate(track.clip_slots):
                    if slot.clip is not None:

                        # match = re.search("(^|[_-])([A-G][A-G#b1-9-]*)$", slot.clip.name)
                        match = re.search("([_-])([A-G][A-G#b1-9-]*)$", slot.clip.name)
                        if match:
                            notes_found_str = match.group(2)
                            notes_found_str = re.sub("[1-9]", "", notes_found_str)
                            notes_found = notes_found_str.split("-")
                            notes = []
                            for note in notes_found:
                                note_midi = self.nameToMIDI(note)
                                if note_midi is not None:
                                    notes.append(note_midi)
                                else:
                                    log(" %s (%s): invalid notes" % (slot.clip.name, track.name))

                            # in case we have spurious/nonsense notes, filter them out
                            notes = filter(lambda n: n is not None, notes)
                            # log(" - %s: found notes: %s" % (slot.clip.name, notes))

                            self.clip_notes_cache[track_index][clip_index] = notes
                        else:
                            self.clip_notes_cache[track_index][clip_index] = None
                            slot.clip.muted = False
            log("filtered clips (took %.3fs)" % (time.time() - t0))
        except Exception, e:
            log("Exception: %s" % e)

    def soloTrackCB(self, msg, source):
        """Called when a /live/solo message is received.

        Messages:
        /live/solo     (int track)   Solos track number track
        """
        ty = msg[0] == '/live/return/solo' and 1 or 0
        track = msg[2]
        
        if len(msg) == 4:
            if msg[3] == 1:
                LiveUtils.soloTrack(track, ty)
            else:
                LiveUtils.unsoloTrack(track, ty)
            
        elif len(msg) == 3:
            if ty == 1:
                status = LiveUtils.getSong().return_tracks[track].solo
                self.oscEndpoint.send("/live/return/solo", (track, int(status)))
                
            else:
                status = LiveUtils.getTrack(track).solo
                self.oscEndpoint.send("/live/solo", (track, int(status)))
            
    def volumeCB(self, msg, source):
        """Called when a /live/volume message is received.

        Messages:
        /live/volume     (int track)                            Returns the current volume of track number track as: /live/volume (int track, float volume(0.0 to 1.0))
        /live/volume     (int track, float volume(0.0 to 1.0))  Sets track number track's volume to volume
        """
        if msg[0] == '/live/return/volume':
            ty = 1
        elif msg[0] == '/live/master/volume':
            ty = 2
        else:
            ty = 0
        
        if len(msg) == 2 and ty == 2:
            self.oscEndpoint.send("/live/master/volume", LiveUtils.getSong().master_track.mixer_device.volume.value)
        
        elif len(msg) == 3 and ty == 2:
            volume = float(msg[2])
            LiveUtils.getSong().master_track.mixer_device.volume.value = volume
        
        elif len(msg) == 4:
            track = int(msg[2])
            volume = float(msg[3])
            
            if ty == 0:
                LiveUtils.trackVolume(track, volume)
            elif ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.volume.value = volume

        elif len(msg) == 3:
            track = int(msg[2])

            if ty == 1:
                self.oscEndpoint.send("/live/return/volume", (track, LiveUtils.getSong().return_tracks[track].mixer_device.volume.value))
            
            else:
                self.oscEndpoint.send("/live/volume", (track, LiveUtils.trackVolume(track)))
            
    def panCB(self, msg, source):
        """Called when a /live/pan message is received.

        Messages:
        /live/pan     (int track)                            Returns the pan of track number track as: /live/pan (int track, float pan(-1.0 to 1.0))
        /live/pan     (int track, float pan(-1.0 to 1.0))    Sets track number track's pan to pan

        """
        if msg[0] == '/live/return/pan':
            ty = 1
        elif msg[0] == '/live/master/pan':
            ty = 2
        else:
            ty = 0
        
        if len(msg) == 2 and ty == 2:
            self.oscEndpoint.send("/live/master/pan", LiveUtils.getSong().master_track.mixer_device.panning.value)
        
        elif len(msg) == 3 and ty == 2:
            pan = msg[2]
            LiveUtils.getSong().master_track.mixer_device.panning.value = pan
            
        elif len(msg) == 4:
            track = msg[2]
            pan = msg[3]
            
            if ty == 0:
                LiveUtils.trackPan(track, pan)
            elif ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.panning.value = pan
            
        elif len(msg) == 3:
            track = msg[2]
            
            if ty == 1:
                self.oscEndpoint.send("/live/pan", (track, LiveUtils.getSong().return_tracks[track].mixer_device.panning.value))
            
            else:
                self.oscEndpoint.send("/live/pan", (track, LiveUtils.trackPan(track)))

            
    def sendCB(self, msg, source):
        """Called when a /live/send message is received.

        Messages:
        /live/send     (int track, int send)                              Returns the send level of send (send) on track number track as: /live/send (int track, int send, float level(0.0 to 1.0))
        /live/send     (int track, int send, float level(0.0 to 1.0))     Sets the send (send) of track number (track)'s level to (level)

        """
        ty = msg[0] == '/live/return/send' and 1 or 0
        track = msg[2]
        
        if len(msg) == 5:
            send = msg[3]
            level = msg[4]
            if ty == 1:
                LiveUtils.getSong().return_tracks[track].mixer_device.sends[send].value = level
            
            else:
                LiveUtils.trackSend(track, send, level)
        
        elif len(msg) == 4:
            send = msg[3]
            if ty == 1:
                self.oscEndpoint.send("/live/return/send", (track, send, float(LiveUtils.getSong().return_tracks[track].mixer_device.sends[send].value)))

            else:
                self.oscEndpoint.send("/live/send", (track, send, float(LiveUtils.trackSend(track, send))))
            
        elif len(msg) == 3:
            if ty == 1:
                sends = LiveUtils.getSong().return_tracks[track].mixer_device.sends
            else:
                sends = LiveUtils.getSong().tracks[track].mixer_device.sends
                
            so = [track]
            for i in range(len(sends)):
                so.append(i)
                so.append(float(sends[i].value))
                
            if ty == 1:
                self.oscEndpoint.send("/live/return/send", tuple(so))
            else:
                self.oscEndpoint.send("/live/send", tuple(so))
                
        
            
    def pitchCB(self, msg, source):
        """Called when a /live/pitch message is received.

        Messages:
        /live/pitch     (int track, int clip)                                               Returns the pan of track number track as: /live/pan (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))
        /live/pitch     (int track, int clip, int coarse(-48 to 48), int fine (-50 to 50))  Sets clip number clip in track number track's pitch to coarse / fine

        TODO: Unlike other callbacks, this does not include the track/pitch indices.

        """
        if len(msg) == 6:
            track = msg[2]
            clip = msg[3]
            coarse = msg[4]
            fine = msg[5]
            LiveUtils.clipPitch(track, clip, coarse, fine)
        if len(msg) ==4:
            track = msg[2]
            clip = msg[3]
            self.oscEndpoint.send("/live/pitch", LiveUtils.clipPitch(track, clip))

    def trackJump(self, msg, source):
        """Called when a /live/track/jump message is received.

        Messages:
        /live/track/jump     (int track, float beats)   Jumps in track's currently running session clip by beats
        """
        if len(msg) == 4:
            track = msg[2]
            beats = msg[3]
            track = LiveUtils.getTrack(track)
            track.jump_in_running_session_clip(beats)

    def trackInfoCB(self, msg, source):
        """Called when a /live/track/info message is received.

        Messages:
        /live/track/info     (int track)   Returns clip slot status' for all clips in a track in the form /live/track/info (tracknumber, armed  (clipnumber, state, length))
                                           [state: 1 = Has Clip, 2 = Playing, 3 = Triggered]
        """
        clipslots = LiveUtils.getClipSlots()
        
        new = []
        if len(msg) == 3:
            new.append(clipslots[msg[2]])
            tracknum = msg[2] - 1
        else:
            new = clipslots
            tracknum = -1
        
        for track in new:
            tracknum = tracknum + 1
            clipnum = -1
            tmptrack = LiveUtils.getTrack(tracknum)
            foldable = tmptrack.is_foldable and 1 or 0
            armed = (not foldable and tmptrack.arm) and 1 or 0
            li = [tracknum, foldable, armed]
            for clipSlot in track:
                clipnum = clipnum + 1
                li.append(clipnum);
                if clipSlot.clip != None:
                    clip = clipSlot.clip
                    if clip.is_playing == 1:
                        li.append(2)
                        li.append(clip.length)
                        
                    elif clip.is_triggered == 1:
                        li.append(3)
                        li.append(clip.length)
                        
                    else:
                        li.append(1)
                        li.append(clip.length)
                else:
                    li.append(0)
                    li.append(0.0)
                    
            tu = tuple(li)
            
            self.oscEndpoint.send("/live/track/info", tu)


    def undoCB(self, msg, source):
        """Called when a /live/undo message is received.
        
        Messages:
        /live/undo      Requests the song to undo the last action
        """
        LiveUtils.getSong().undo()
        
    def redoCB(self, msg, source):
        """Called when a /live/redo message is received.
        
        Messages:
        /live/redo      Requests the song to redo the last action
        """
        LiveUtils.getSong().redo()
        
    def playClipSlotCB(self, msg, source):
        """Called when a /live/play/clipslot message is received.
        
        Messages:
        /live/play/clipslot     (int track, int clip)   Launches clip number clip in track number track
        """
        if len(msg) == 4:
            track_num = msg[2]
            clip_num = msg[3]
            track = LiveUtils.getTrack(track_num)
            clipslot = track.clip_slots[clip_num]
            clipslot.fire()

    def viewSceneCB(self, msg, source):
        """Called when a /live/scene/view message is received.
        
        Messages:
        /live/scene/view     (int track)      Selects a track to view
        """
        
        if len(msg) == 3:
            scene = msg[2]
            LiveUtils.getSong().view.selected_scene = LiveUtils.getSong().scenes[scene]
            
    def viewTrackCB(self, msg, source):
        """Called when a /live/track/view message is received.
        
        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/view' and 1 or 0
        track_num = msg[2]
        
        if len(msg) == 3:
            if ty == 1:
                track = LiveUtils.getSong().return_tracks[track_num]
            else:
                track = LiveUtils.getSong().tracks[track_num]
                
            LiveUtils.getSong().view.selected_track = track
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
                
            #track.view.select_instrument()
            
    def mviewTrackCB(self, msg, source):
        """Called when a /live/master/view message is received.
        
        Messages:
        /live/track/view     (int track)      Selects a track to view
        """
        track = LiveUtils.getSong().master_track

        LiveUtils.getSong().view.selected_track = track
        Live.Application.get_application().view.show_view("Detail/DeviceChain")        
        
        #track.view.select_instrument()
        
    def viewClipCB(self, msg, source):
        """Called when a /live/clip/view message is received.
        
        Messages:
        /live/clip/view     (int track, int clip)      Selects a track to view
        """
        track = LiveUtils.getSong().tracks[msg[2]]
        
        if len(msg) == 4:
            clip  = msg[3]
        else:
            clip  = 0
        
        LiveUtils.getSong().view.selected_track = track
        LiveUtils.getSong().view.detail_clip = track.clip_slots[clip].clip
        Live.Application.get_application().view.show_view("Detail/Clip")  

    def detailViewCB(self, msg, source):
        """Called when a /live/detail/view message is received. Used to switch between clip/track detail

        Messages:
        /live/detail/view (int) Selects view where 0=clip detail, 1=track detail
        """
        if len(msg) == 3:
            if msg[2] == 0:
                Live.Application.get_application().view.show_view("Detail/Clip")
            elif msg[2] == 1:
                Live.Application.get_application().view.show_view("Detail/DeviceChain")

    def viewDeviceCB(self, msg, source):
        """Called when a /live/track/device/view message is received.
        
        Messages:
        /live/track/device/view     (int track)      Selects a track to view
        """
        ty = msg[0] == '/live/return/device/view' and 1 or 0
        track_num = msg[2]
        
        if len(msg) == 4:
            if ty == 1:
                track = LiveUtils.getSong().return_tracks[track_num]
            else:
                track = LiveUtils.getSong().tracks[track_num]

            LiveUtils.getSong().view.selected_track = track
            LiveUtils.getSong().view.select_device(track.devices[msg[3]])
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
            
    def mviewDeviceCB(self, msg, source):
        track = LiveUtils.getSong().master_track
        
        if len(msg) == 3:
            LiveUtils.getSong().view.selected_track = track
            LiveUtils.getSong().view.select_device(track.devices[msg[2]])
            Live.Application.get_application().view.show_view("Detail/DeviceChain")
        
    def overdubCB(self, msg, source):
        """Called when a /live/overdub message is received.
        
        Messages:
        /live/overdub     (int on/off)      Enables/disables overdub
        """        
        if len(msg) == 3:
            overdub = msg[2]
            LiveUtils.getSong().overdub = overdub

    def stateCB(self, msg, source):
        """Called when a /live/state is received.
        
        Messages:
        /live/state                    Returns the current tempo and overdub status
        """
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            tempo = LiveUtils.getTempo()
            overdub = LiveUtils.getSong().overdub
            self.oscEndpoint.send("/live/state", (tempo, int(overdub)))
        
    def clipInfoCB(self,msg):
        """Called when a /live/clip/info message is received.
        
        Messages:
        /live/clip/info     (int track, int clip)      Gets the status of a single clip in the form  /live/clip/info (tracknumber, clipnumber, state)
                                                       [state: 1 = Has Clip, 2 = Playing, 3 = Triggered]
        """
        
        if len(msg) == 4:
            trackNumber = msg[2]
            clipNumber = msg[3]    
            
            clip = LiveUtils.getClip(trackNumber, clipNumber)
            
            playing = 0
            
            if clip != None:
                playing = 1
                
                if clip.is_playing == 1:
                    playing = 2
                elif clip.is_triggered == 1:
                    playing = 3

            self.oscEndpoint.send("/live/clip/info", (trackNumber, clipNumber, playing))
        
        return

    def muteClipCB(self, msg, source):
        """Called when a /live/clip/mute message is received.
        
        Messages:
        /live/clip/view     (int track, int clip)      Selects a clip to mute.
        """
        # use LogServer.py to read logs
        # log("muting")
        trackNumber = msg[2]
        clipNumber = msg[3]
        
        clip = LiveUtils.getClip(trackNumber, clipNumber)
        log("clip is %s (vars %s)" % (clip, vars(clip)))
        if len(msg) == 5:
            muted = msg[4]
            clip.muted = bool(muted)
        else:
            self.oscEndpoint.send("/live/clip/mute", (trackNumber, clipNumber, int(clip.muted)))
        
    def deviceCB(self, msg, source):
        ty = msg[0] == '/live/return/device' and 1 or 0
        track = msg[2]
    
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            
            if ty == 1:
                params = LiveUtils.getSong().return_tracks[track].devices[device].parameters
            else:
                params = LiveUtils.getSong().tracks[track].devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))
            
            self.oscEndpoint.send(ty == 1 and "/live/return/device/allparam" or "/live/device/allparam", tuple(po))
    
        elif len(msg) == 5:
            device = msg[3]
            param  = msg[4]
            
            if ty == 1:
                p = LiveUtils.getSong().return_tracks[track].devices[device].parameters[param]
            else: 
                p = LiveUtils.getSong().tracks[track].devices[device].parameters[param]
        
            self.oscEndpoint.send(ty == 1 and "/live/return/device/param" or "/live/device/param", (track, device, param, p.value, str(p.name)))
    
    
        elif len(msg) == 6:
            device = msg[3]
            param  = msg[4]
            value  = msg[5]
        
            if ty == 1:
                LiveUtils.getSong().return_tracks[track].devices[device].parameters[param].value = value
            else:
                LiveUtils.getSong().tracks[track].devices[device].parameters[param].value = value

    def devicerangeCB(self, msg, source):
        ty = msg[0] == '/live/return/device/range' and 1 or 0
        track = msg[2]
    
        if len(msg) == 4:
            device = msg[3]
            po = [track, device]
            
            if ty == 1:
                params = LiveUtils.getSong().return_tracks[track].devices[device].parameters
            else:
                params = LiveUtils.getSong().tracks[track].devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].min)
                po.append(params[i].max)
            
            self.oscEndpoint.send(ty == 1 and "/live/return/device/range" or "/live/device/range", tuple(po))
    
        elif len(msg) == 5:
            device = msg[3]
            param  = msg[4]
            
            if ty == 1:
                p = LiveUtils.getSong().return_tracks[track].devices[device].parameters[param]
            else: 
                p = LiveUtils.getSong().tracks[track].devices[device].parameters[param]
        
            self.oscEndpoint.send(ty == 1 and "/live/return/device/range" or "/live/device/range", (track, device, param, p.min, p.max))
                
    def devicelistCB(self, msg, source):
        ty = msg[0] == '/live/return/devicelist' and 1 or 0

        track = msg[2]
    
        if len(msg) == 3:
            do = [track]
            
            if ty == 1:
                devices = LiveUtils.getSong().return_tracks[track].devices
            else:
                devices = LiveUtils.getSong().tracks[track].devices
        
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))
            
            self.oscEndpoint.send(ty == 1 and "/live/return/devicelist" or "/live/devicelist", tuple(do))

    def mdeviceCB(self, msg, source):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            
            params = LiveUtils.getSong().master_track.devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(float(params[i].value))
                po.append(str(params[i].name))
            
            self.oscEndpoint.send("/live/master/device", tuple(po))
    
        elif len(msg) == 4:
            device = msg[2]
            param  = msg[3]
            
            p = LiveUtils.getSong().master_track.devices[device].parameters[param]
        
            self.oscEndpoint.send("/live/master/device", (device, param, p.value, str(p.name)))
    
        elif len(msg) == 5:
            device = msg[2]
            param  = msg[3]
            value  = msg[4]
        
            LiveUtils.getSong().master_track.devices[device].parameters[param].value = value

    def mdevicerangeCB(self, msg, source):
        if len(msg) == 3:
            device = msg[2]
            po = [device]
            
            params = LiveUtils.getSong().master_track.devices[device].parameters
    
            for i in range(len(params)):
                po.append(i)
                po.append(params[i].max)
                po.append(params[i].min)
            
            self.oscEndpoint.send("/live/master/device/range", tuple(po))
    
        elif len(msg) == 4:
            device = msg[2]
            param  = msg[3]
            
            p = LiveUtils.getSong().master_track.devices[device].parameters[param]
        
            self.oscEndpoint.send("/live/master/device/range", (device, param, p.min, p.max))
            
    def mdevicelistCB(self, msg, source):
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            do = []
            devices = LiveUtils.getSong().master_track.devices
        
            for i in range(len(devices)):
                do.append(i)
                do.append(str(devices[i].name))
            
            self.oscEndpoint.send("/live/master/devicelist", tuple(do))            
            
            
    def crossfaderCB(self, msg, source):
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscEndpoint.send("/live/master/crossfader", float(LiveUtils.getSong().master_track.mixer_device.crossfader.value))
        
        elif len(msg) == 3:
            val = msg[2]
            LiveUtils.getSong().master_track.mixer_device.crossfader.value = val


    def loopStateCB(self, msg, source):
        type = msg[0] == '/live/clip/loopstate_id' and 1 or 0
    
        trackNumber = msg[2]
        clipNumber = msg[3]
    
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send("/live/clip/loopstate", (trackNumber, clipNumber, int(LiveUtils.getClip(trackNumber, clipNumber).looping)))
            else:
                self.oscEndpoint.send("/live/clip/loopstate", (int(LiveUtils.getClip(trackNumber, clipNumber).looping)))    
        
        elif len(msg) == 5:
            loopState = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).looping =  loopState

    def loopStartCB(self, msg, source):
        type = msg[0] == '/live/clip/loopstart_id' and 1 or 0
        
        trackNumber = msg[2]
        clipNumber = msg[3]
    
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send("/live/clip/loopstart", (trackNumber, clipNumber, float(LiveUtils.getClip(trackNumber, clipNumber).loop_start)))    
            else:
                self.oscEndpoint.send("/live/clip/loopstart", (float(LiveUtils.getClip(trackNumber, clipNumber).loop_start)))    
    
        elif len(msg) == 5:
            loopStart = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).loop_start = loopStart
            
    def loopEndCB(self, msg, source):
        type = msg[0] == '/live/clip/loopend_id' and 1 or 0
    
        trackNumber = msg[2]
        clipNumber = msg[3]    
        if len(msg) == 4:
            if type == 1:
                self.oscEndpoint.send("/live/clip/loopend", (trackNumber, clipNumber, float(LiveUtils.getClip(trackNumber, clipNumber).loop_end)))
            else:
                self.oscEndpoint.send("/live/clip/loopend", (float(LiveUtils.getClip(trackNumber, clipNumber).loop_end)))    
        
        elif len(msg) == 5:
            loopEnd = msg[4]
            LiveUtils.getClip(trackNumber, clipNumber).loop_end =  loopEnd

    def quantizationCB(self, msg, source):
        if len(msg) == 2 or (len(msg) == 3 and msg[2] == "query"):
            self.oscEndpoint.send("/live/quantization", int(LiveUtils.getSong().clip_trigger_quantization))
        
        elif len(msg) == 3:
            LiveUtils.getSong().clip_trigger_quantization = msg[2]

    def distributeGroupsCB(self, msg, source):
        if len(msg) == 3:
            outputs = range(1, msg[2] + 1)
        else:
            outputs = range(1, 64)
        index = 0
        for track in LiveUtils.getTracks():
            if track.is_foldable:
                output = outputs[index]
                index = (index + 1) % len(outputs)
                log(" - rerouting group track %s (%d), current subrouting = %s" % (track, index, track.current_output_sub_routing))
                track.current_output_routing = "Ext. Out"
                track.current_output_sub_routing = str(output)

    def playGroupSceneCB(self, msg, source):
        if len(msg) == 4:
            track_index = msg[2]
            clip_index = msg[3]
            tracks = LiveUtils.getTracks()
            group = tracks[track_index]
            if group.is_foldable:
                target_tracks = []
                for track in tracks[track_index+1:]:
                    if track.is_foldable:
                        break
                    else:
                        target_tracks.append(track)
                for index, track in enumerate(target_tracks):
                    for cindex, clipslot in enumerate(track.clip_slots[clip_index:]):
                        if clipslot.clip is None:
                            track.stop_all_clips()
                            break
                        elif not clipslot.clip.muted:
                            clipslot.fire()
                            break
            else:
                log("playGroupScene: Target is not a group (ID %d)" % track_index)
        else:
            log("playGroupScene: Too few args")
