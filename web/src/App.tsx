import { useCallback, useState } from "react";
import "./App.css";
import { UnauthenticatedTemplate } from "./component/UnauthenticatedTemplate";
import { AuthenticatedTemplate } from "./component/AuthenticatedTemplate";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = useCallback(() => {
    setLoggedIn(true);
  }, []);

  // login check:
  // send a request to a protected endpoint on the server for the user's info
  // if the response is successful, set loggedIn to true and redirect to protected route
  console.log(`logged in? ${loggedIn}`);

  // if (!loggedIn) {
  return <UnauthenticatedTemplate loginCallback={handleLogin} />;
  // }

  // return <AuthenticatedTemplate />;
}

export default App;
