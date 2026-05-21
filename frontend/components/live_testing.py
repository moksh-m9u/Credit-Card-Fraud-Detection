import streamlit as st
import requests
import json

def render_live_testing():
    st.markdown('<div class="section-header">Live Backend Integration Testing</div>', unsafe_allow_html=True)
    st.info("The UI is currently interfacing with the deployed FastAPI backend on Render. It may take 30-60s to wake up on the first request.")
    
    test_type = st.radio("Select Testing Mode", ["Single Prediction", "Batch Prediction (JSON)"], horizontal=True)
    
    if test_type == "Single Prediction":
        API_URL_SINGLE = "https://credict-card-server.onrender.com/predict"
        st.write(f"**Endpoint:** `{API_URL_SINGLE}`")
        
        input_method = st.selectbox("Input Method", ["Interactive Form", "Raw Comma-Separated Values (Kaggle Format)"])
        
        if input_method == "Interactive Form":
            scenario_choice = st.selectbox(
                "Load Example Scenario", 
                ["Custom Single Transaction", "Single Fraudulent Transaction", "Single Normal Transaction"]
            )
            
            if scenario_choice == "Single Fraudulent Transaction":
                def_vals = [-4.289254, -2.772272, -2.899907, 3.997906, -2.830056, -1.609851, 3.202033, -1.140747, 0.00]
            elif scenario_choice == "Single Normal Transaction":
                def_vals = [-0.311169, 0.090794, -0.617800, 1.378155, 0.207971, 2.536346, -0.551599, -0.470400, 149.62]
            else:
                def_vals = [0.0] * 9
                
            with st.form("prediction_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    v14 = st.number_input("V14", value=def_vals[0], format="%.6f")
                    v10 = st.number_input("V10", value=def_vals[1], format="%.6f")
                    v12 = st.number_input("V12", value=def_vals[2], format="%.6f")
                with col2:
                    v4 = st.number_input("V4", value=def_vals[3], format="%.6f")
                    v17 = st.number_input("V17", value=def_vals[4], format="%.6f")
                    v3 = st.number_input("V3", value=def_vals[5], format="%.6f")
                with col3:
                    v11 = st.number_input("V11", value=def_vals[6], format="%.6f")
                    v16 = st.number_input("V16", value=def_vals[7], format="%.6f")
                    amount = st.number_input("Amount", value=def_vals[8], format="%.2f")
                    
                submitted = st.form_submit_button("Predict Fraud")
                
                if submitted:
                    payload = {
                        "V14": v14, "V10": v10, "V12": v12, "V4": v4, 
                        "V17": v17, "V3": v3, "V11": v11, "V16": v16, "Amount": amount
                    }
                    
                    with st.spinner("Connecting to FastAPI backend..."):
                        try:
                            response = requests.post(API_URL_SINGLE, json=payload, timeout=120)
                            if response.status_code == 200:
                                result = response.json()
                                st.success("Prediction retrieved successfully!")
                                pred_col1, pred_col2 = st.columns(2)
                                with pred_col1:
                                    if result.get("prediction") == 1:
                                        st.error(f"Prediction: {result.get('label').upper()}")
                                    else:
                                        st.success(f"Prediction: {result.get('label').upper()}")
                                with pred_col2:
                                    st.metric("Confidence", f"{result.get('confidence'):.2%}")
                                st.json(result)
                            else:
                                st.error(f"Error from API: {response.status_code}")
                        except Exception as e:
                            st.error(f"Connection failed: {e}")

        else:
            st.markdown("Paste an entire row from the dataset (30 values: Time, V1-V28, Amount). If you include the Class label, it will be automatically ignored.")
            example_csv = '0,-1.3598071336738,-0.0727811733098497,2.53634673796914,1.37815522427443,-0.338320769942518,0.462387777762292,0.239598554061257,0.0986979012610507,0.363786969611213,0.0907941719789316,-0.551599533260813,-0.617800855762348,-0.991389847235408,-0.311169353699879,1.46817697209427,-0.470400525259478,0.207971241929242,0.0257905801985591,0.403992960255733,0.251412098239705,-0.018306777944153,0.277837575558899,-0.110473910188767,0.0669280749146731,0.128539358273528,-0.189114843888824,0.133558376740387,-0.0210530534538215,149.62'
            csv_input = st.text_area("Comma-Separated Input", placeholder=example_csv, height=100)
            
            if st.button("Predict Fraud"):
                if csv_input.strip():
                    try:
                        clean_vals = [x.strip().replace('"', '').replace("'", "") for x in csv_input.split(',')]
                        if len(clean_vals) not in [30, 31]:
                            st.error(f"Expected 30 or 31 values, got {len(clean_vals)}.")
                        else:
                            parsed_vals = [float(x) for x in clean_vals]
                            headers = ["Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount"]
                            
                            payload = {headers[i]: parsed_vals[i] for i in range(30)}
                                
                            if len(clean_vals) == 31:
                                st.info("💡 Notice: We detected 31 values. The 31st value (Class) was gracefully ignored.")
                                
                            with st.spinner("Connecting..."):
                                response = requests.post(API_URL_SINGLE, json=payload, timeout=120)
                                if response.status_code == 200:
                                    result = response.json()
                                    st.success("Prediction retrieved successfully!")
                                    pred_col1, pred_col2 = st.columns(2)
                                    with pred_col1:
                                        if result.get("prediction") == 1:
                                            st.error(f"Prediction: {result.get('label').upper()}")
                                        else:
                                            st.success(f"Prediction: {result.get('label').upper()}")
                                    with pred_col2:
                                        st.metric("Confidence", f"{result.get('confidence'):.2%}")
                                    st.json(result)
                                else:
                                    st.error(f"Error: {response.status_code}")
                    except ValueError:
                        st.error("Parsing Error: Make sure values are separated by commas.")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

    elif test_type == "Batch Prediction (JSON)":
        API_URL_BATCH = "https://credict-card-server.onrender.com/predict/batch"
        st.write(f"**Endpoint:** `{API_URL_BATCH}`")
        
        default_batch_json = '''[
  {
    "V14": -4.289254, "V10": -2.772272, "V12": -2.899907, "V4": 3.997906,
    "V17": -2.830056, "V3": -1.609851, "V11": 3.202033, "V16": -1.140747, "Amount": 0.00
  },
  {
    "V14": -0.311169, "V10": 0.090794, "V12": -0.617800, "V4": 1.378155,
    "V17": 0.207971, "V3": 2.536346, "V11": -0.551599, "V16": -0.470400, "Amount": 149.62
  }
]'''
        batch_input = st.text_area("JSON Payload", value=default_batch_json, height=250)
        
        if st.button("Run Batch Prediction"):
            try:
                batch_payload = json.loads(batch_input)
                with st.spinner("Connecting to FastAPI backend..."):
                    response = requests.post(API_URL_BATCH, json=batch_payload, timeout=120)
                    if response.status_code == 200:
                        st.success("Batch prediction completed!")
                        st.json(response.json())
                    else:
                        st.error(f"Error from API: {response.status_code}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format.")
            except Exception as e:
                st.error(f"Connection failed: {e}")
