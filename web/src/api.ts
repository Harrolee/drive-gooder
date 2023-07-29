import axios from "axios";
import { ReactMicStopEvent } from "react-mic";
import { BACKEND_URL } from "./constants";

type AssistantPayload = { data: Blob };
export type AssistantResponse = {
    transcription: string;
    llmResponse: string;
};
export type AssistantSpeechResponse = {
    data: Blob;
};

export async function saveRecording(
    recordedData: ReactMicStopEvent
): Promise<AssistantResponse | void> {
    const formData = new FormData();
    formData.append("audio_data", recordedData.blob, "temp_recording");
    try {
        // @ts-ignore
        const { data } = await axios
            .post<AssistantPayload>(`${BACKEND_URL}/talk_llm`, formData, {
                headers: {
                    "content-type": "multipart/form-data",
                    "Access-Control-Allow-Origin": "*",
                },
            })
            .catch((error) => {
                console.error(error);
            });
        console.log(data);
        console.log(JSON.stringify(data));
        return data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.log("error message: ", error.message);
            // 👇️ error: AxiosError<any, any>
            //   return error.message;
        } else {
            console.log("Could not send recording: ", error);
            //   return "Could not send recording";
        }
    }
}

export async function getSpeech(
    recordedData: ReactMicStopEvent
): Promise<ArrayBuffer | undefined> {
    const formData = new FormData();
    formData.append("audio_data", recordedData.blob, "temp_recording");
    try {
        // @ts-ignore
        const { data } = await axios
            .post<AssistantPayload>(`${BACKEND_URL}/sound_llm`, formData, {
                headers: {
                    "content-type": "multipart/form-data",
                    "Access-Control-Allow-Origin": "*",
                },
                responseType: "arraybuffer",
            })
            .catch((error) => {
                console.error(error);
            });
        return data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.log("error message: ", error.message);
            // 👇️ error: AxiosError<any, any>
            //   return error.message;
        } else {
            console.log("Could not send recording: ", error);
            //   return "Could not send recording";
        }
        return undefined;
    }
}
