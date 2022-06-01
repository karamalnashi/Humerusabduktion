# "ebrain/armbasistraining_digital"
abt_configuration_dict = {
    "exercise_number": 1,
    "side": "left",
    "count": "10",
    "patient_movement_range": 0.75,

}





#################################################################################################
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
topic ="ebrain/#"
ja= {
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
        "answer_topic": "ebrain/ja",
        "layout_type": "ja",
        "stateID": "0_start",
        "abt_configuration_dict":{
        "exercise_number": 2,
        "side": "left",
        "count": "10",
        "patient_movement_range": 0.75,
      }
     }


}



####################################################################################

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
