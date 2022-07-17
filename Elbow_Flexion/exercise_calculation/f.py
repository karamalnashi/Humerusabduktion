# "ebrain/armbasistraining_digital"

#die Nachrichten, die Anwendung erhalten soll
#################################################################################################

#Die Nachricht, die die Anwendung dazu veranlasst, zu arbeiten und nach dem Patienten zu suchen
start= {
    "api_version": "v0.1.0",
    "time": 1638367683.530698,
    "time_hr": "2021-12-01T15:08:03.530698",
    "sender_CID": "DialogEngine1",
    "message_type": "interaction",
    "message_uuid": "DialogEngine1-interaction19635f4c-52b0-11ec-956f-f8b156cd740c",

    "content": {
        "say": "",
        "image": "",
        "answers": [""],
        "answer_topic": "ebrain/start",
        "layout_type": "start",
        "stateID": "0_start"
     }

}

##########################################################################################
#Diese Meldung soll die Frage des Programms beantworten, ob dies der richtige Patient ist oder nicht, der auf der Kamera erscheint.
#Die Informationen des Patienten werden über diese Nachricht gesendet
ja= {
    "api_version": "v0.1.0",
    "time": 1638367683.530698,
    "time_hr": "2021-12-01T15:08:03.530698",
    "sender_CID": "Dialo\gEngine1",
    "message_type": "interaction",
    "message_uuid": "DialogEngine1-interaction19635f4c-52b0-11ec-956f-f8b156cd740c",

    "content": {
        "say": "",
        "image": "",
        "answers": [""],
        "answer_topic": "ebrain/ja",
        "layout_type": "ja",
        "stateID": "0_start",
        "abt_configuration_dict":{
        "exercise_number": 1,
        "side": "left",
        "count": "5",
        "patient_movement_range": 1,
        "time_pause":12
      }
     }
}


####################################################################################
#Diese Meldung dient nach Beendigung des Trainings dazu, die Trainingsarbeit zu stoppen
end= {
    "api_version": "v0.1.0",
    "time": 1638367683.530698,
    "time_hr": "2021-12-01T15:08:03.530698",
    "sender_CID": "DialogEngine1",
    "message_type": "interaction",
    "message_uuid": "DialogEngine1-interaction19635f4c-52b0-11ec-956f-f8b156cd740c",

    "content": {
        "say": "",
        "image": "",
        "answers": [""],
        "answer_topic": "ebrain/end",
        "layout_type": "end",
        "stateID": "0_start"
     }

}
