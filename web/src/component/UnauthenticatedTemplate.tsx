import { getUserInfo } from "../api";
import OAuthLogin from "./OAuthLogin";

export interface UnauthenticatedTemplateProps {
  loginCallback: VoidFunction;
}

export function UnauthenticatedTemplate(props: UnauthenticatedTemplateProps) {
  getUserInfo().then((userInfo) => {
    console.log(`userInfo: ${JSON.stringify(userInfo)}`);
    if (userInfo?.authenticated === "true") {
      props.loginCallback();
    }
    // else, user is not logged in
  });

  return <OAuthLogin loginCallback={props.loginCallback} />;
}
