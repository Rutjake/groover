-- Script Version 1.0
-- Console
function Msg(str)
    reaper.ShowConsoleMsg(tostring(str) .. "\n")
  end

-- Hakee valitun MIDI-itemin ja aktiivisen taken
local hwnd = reaper.MIDIEditor_GetActive()
local take = reaper.MIDIEditor_GetTake(hwnd)

--[[
    timingVariation: 20 = +- 20ms, Eli yhteensä 40ms 
    swingAmount: Swingin määrä (0 = ei swingiä, 1 = täysi swing)
    handedness: Oletko oikea- vai vasenkätinen? (right/left)
    handSrenght: Voimakkuus Ero Käsien Välillä
    velocityVariation: Kuinka Paljon Varioidaan Iskujen Voimakkuutta +-10 Eli Yhtensä 20
    maxVelocity: Rumpalin maksimi voimakkuus (0-127)
    minVelocity: Rumpalin minimi voimakkuus (0-127)
    useHandednessFeature: Otetaan käyttöön kätisyys (true = käytössä/false = ei käytössä)
    ]]

--Asetukset (Säädä Tarpeen Mukaan)
local timingVariation = 0
local swingAmount = 0.1
local handedness = "right"
local handStrenght = 10
local velocityVariation = 5
local maxVelocity = 115
local minVelocity = 50
local useHandednessFeature = False

-- Msg(hwnd)
-- Msg(take)
--local item = reaper.GetSelectedMediaItem(0, 0)

function countNotes(take)
    retval, notes, ccs, sysex = reaper.MIDI_CountEvts(take) -- lasketaan nuotit(tapahtuma)
    i = 0
    check = 0
    notes_selected=0

    for i=0, notes-1 do
    retval, selected, muted, startPPQ, endppq, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
    if selected == true then -- etsitään valittut nuotit
        check = check + 1 -- jos niitä löytyy lisätään ne check muuttujaan
        
    end
    i=i+1
    end
    -- Msg(check)
    return check
end

local selectedNoteCount = countNotes(take)

-- Swing ja Time Variaatio Funktio
function swingAndVariation(take, swingAmount, timingVariation)
    
    retval, notes, css, sysex = reaper.MIDI_CountEvts(take)
    -- Lasketaan nuottien kokonaismäärä
    local numNotes = reaper.MIDI_CountEvts(take)
    -- Haetaan Projektin Tempo
    local tempo = reaper.Master_GetTempo()

    --Msg("Tempo:" .. tempo)

    -- Käydään läpi kaikki nuotit
    for i = 0, numNotes - 1 do
        local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
        
        if selected then
            realStartPpq = startppqpos / 960
            -- Lasketaan sekunnit per PPQ ja muutetaan sekunneiksi
                --Aloitus aika
            local secondsPerPPQ = 60 / tempo
            local startTimeInMs = realStartPpq * secondsPerPPQ
            Msg("Start Time: " .. startTimeInMs)
            -- Swingi
            local swingOffset = swingAmount / 100 * math.sin(math.rad(startTimeInMs * 90)) * startTimeInMs / 10
    
            -- Timing Variaatio
            local randomOffset = math.random(-timingVariation, timingVariation) / 1000
            
            -- Lisätään Variaatio Ja Swing
            local newStartTime = startTimeInMs + randomOffset + swingOffset


            --Muutetaan Ms takaisin PPQ arvoksi 
            local newStartTimePPQ = newStartTime * 960 / (60 / tempo)
            Msg(newStartTime)
            --Päivitetään nuotin aloitus aika
            reaper.MIDI_SetNote(take, i, 0, muted, newStartTimePPQ, endppqpos, chan, pitch, vel)

            --Msg("Vanha Aika: " .. startTimeInMs)
            --Msg("Uusi Aika: " .. newStartTime)
            --Msg(realStartPpq)
            --Msg(newStartTimePPQ)
        end
        
    end
end

-- Velocity Variation
function hitVariation(take, velocityVariation, minVelocity, maxVelocity)

    retval, notes, css, sysex = reaper.MIDI_CountEvts(take)

    -- Lasketaan nuottien kokonaismäärä
    local numNotes = reaper.MIDI_CountEvts(take)

    -- Käydään läpi kaikki nuotit
    for i = 0, numNotes - 1 do
        local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
        
        if selected then
            --Threshold
            local newMaxVelocity = maxVelocity - velocityVariation
            -- Asetetaan Velocity
            local randomOffset = math.random(-velocityVariation, velocityVariation)
            local newVelocity = math.max(minVelocity, math.min(maxVelocity, newMaxVelocity + randomOffset))
            --Msg(" Vel: " .. vel .. " randomOffset: " .. randomOffset .. " New Velocity: " .. newVelocity)
            
            -- Päivitetään Velocity
            reaper.MIDI_SetNote(take, i, selected, muted, startppqpos, endppqpos, chan, pitch, newVelocity)
        end
    end
end

function applyHandedness(take, handedness, handStrenght)

    retval, notes, css, sysex = reaper.MIDI_CountEvts(take)

    -- Lasketaan nuottien kokonaismäärä
    local numNotes = reaper.MIDI_CountEvts(take)

    local lastPlayedHand = "left" -- Viimeeksi käytetty käsi

    -- Käydään läpi kaikki nuotit
    for i = 0, numNotes - 1 do
        local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
        
        if selected then
        -- Tarkista kätisyys ja lisää voimakkuutta hallitsevalle puolelle
            if handedness == "right" then
                -- Oikeakätinen soittaja
                if lastPlayedHand == "right" then
                    -- Edellinen nuotti soitettiin oikealla, nyt vasemmalla
                    vel = math.max(0, vel - handStrenght)
                else
                    -- Edellinen nuotti soitettiin vasemmalla, nyt oikealla
                    vel = math.min(127, vel + handStrenght)
                end
            else --Vasenkätinen soittaja
                if lastPlayedHand == "right" then
                    -- Edellinen nuotti soitettiin oikealla (vasenkätiselle vasemmalla), nyt vasemmalla (vasenkätiselle oikealla)
                    vel = math.min(127, vel + handStrenght)
                else
                    -- Edellinen nuotti soitettiin vasemmalla (vasenkätiselle oikealla), nyt oikealla (vasenkätiselle vasemmalla)
                    vel = math.max(0, vel - handStrenght)
                end
            end
            lastPlayedHand = lastPlayedHand == "right" and "left" or "right" -- Vaihda käsi
            reaper.MIDI_SetNote(take, i, selected, muted, startppqpos, endppqpos, chan, pitch, vel)
        end
    end
end

function groover()

    -- Velocity Variation
    hitVariation(take, velocityVariation, minVelocity, maxVelocity)

    -- Tarkistetaan onko kätisyys käytössä
    if useHandednessFeature then
        applyHandedness(take, handedness, handStrenght)
    end

    -- Swing And Variation 
    swingAndVariation(take, swingAmount, timingVariation)

end

if selectedNoteCount > 0 then
    groover()
else
    Msg("Valitse vähintään yksi nuotti MIDI-editorissa.")
end

-- Ota vastaan muuttujien parametrit pythonista
function set_parameters(timingVariation, swingAmount, handedness, handStrenght, velocityVariation, maxVelocity, minVelocity, useHandednessFeature)
    --Msg("Saadut parametrit: ")
    --Msg("timingVariation " .. timingVariation )
    
    timingVariation = timingVariation
    swingAmount = swingAmount
    handedness = handedness
    handStrenght = handStrenght
    velocityVariation = velocityVariation
    maxVelocity = maxVelocity
    minVelocity = minVelocity
    useHandednessFeature = useHandednessFeature
end
reaper.UpdateArrange()