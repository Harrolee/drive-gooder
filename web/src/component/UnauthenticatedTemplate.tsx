import { useCallback, useState } from "react";
import { getUserInfo, storeLoginCredentials } from "../api";
// import Login from "./Login";
import OAuthLogin from "./OAuthLogin";
import React from "react";

export interface UnauthenticatedTemplateProps {
  loginCallback: VoidFunction;
}

export function UnauthenticatedTemplate(props: UnauthenticatedTemplateProps) {
  getUserInfo().then((userInfo) => {
    console.log(`userInfo: ${JSON.stringify(userInfo)}`);
    if (userInfo.name !== null) {
      props.loginCallback();
    }
  });

  return <OAuthLogin loginCallback={props.loginCallback} />;
}
