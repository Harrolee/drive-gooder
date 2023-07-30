import { useCallback, useState } from "react";
import "./App.css";
import { UnauthenticatedTemplate } from "./component/UnauthenticatedTemplate";
import { AuthenticatedTemplate } from "./component/AuthenticatedTemplate";

function App() {
    const [loggedIn, setLoggedIn] = useState(false);

    const handleLogin = useCallback(() => {
        setLoggedIn(true);
    }, []);

    if (!loggedIn) {
        return <UnauthenticatedTemplate loginCallback={handleLogin} />;
    }

    return <AuthenticatedTemplate />;
}

export default App;
