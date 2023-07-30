import { useCallback, useState } from "react";
import { storeLoginCredentials } from "../api"
import Login from "./Login";
import React from "react";

export interface UnauthenticatedTemplateProps {
    loginCallback: VoidFunction;
}

export function UnauthenticatedTemplate(props: UnauthenticatedTemplateProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const loginCallback = useCallback(() => {
      storeLoginCredentials(username, password);
      props.loginCallback();
    }, [username, password, props]);

    return <Login
        username={username}
        setUsername={setUsername}
        password={password}
        setPassword={setPassword}
        loginCallback={loginCallback} />
}