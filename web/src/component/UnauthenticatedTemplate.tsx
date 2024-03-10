import { useCallback, useState } from "react";
import { getUserInfo, storeLoginCredentials } from "../api";
// import Login from "./Login";
import OAuthLogin from "./OAuthLogin";
import React from "react";

export interface UnauthenticatedTemplateProps {
  loginCallback: VoidFunction;
}

export function UnauthenticatedTemplate(props: UnauthenticatedTemplateProps) {
  // const [username, setUsername] = useState("");
  // const [password, setPassword] = useState("");

  // const loginCallback = useCallback(() => {
  //   storeLoginCredentials(username, password);
  //   props.loginCallback();
  // }, [username, password, props]);

  getUserInfo().then((userInfo) => {
    console.log(`userInfo: ${JSON.stringify(userInfo)}`);
    if (userInfo !== null) {
      props.loginCallback();
    }
  });

  return <OAuthLogin loginCallback={props.loginCallback} />;
  // <Login
  //     username={username}
  //     setUsername={setUsername}
  //     password={password}
  //     setPassword={setPassword}
  //     loginCallback={loginCallback} />
}
