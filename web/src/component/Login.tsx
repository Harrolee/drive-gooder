import { useCallback } from "react";
import { authenticate } from "../api";

export interface LoginProps {
    username: string;
    setUsername: React.Dispatch<React.SetStateAction<string>>;
    password: string;
    setPassword: React.Dispatch<React.SetStateAction<string>>;
    loginCallback: VoidFunction;
}

export default function Login(props: LoginProps) {
    const handleUsernameChange = useCallback((event: any) => {
        props.setUsername(event.target.value)
    }, [props]);

    const handlePasswordChange = useCallback((event: any) => {
        props.setPassword(event.target.value)
    }, [props]);

    const handleLogin = useCallback(async (event: any) => {
        event.preventDefault();

        if (props.username !== "" && props.password !== "") {
            const success = await authenticate(props.username, props.password);
            if (success) {
                props.loginCallback();
            }
        }
    }, [props]);

    return <div>
        <form onSubmit={handleLogin}>
            <div>
                <label>Username</label>
            </div>
            <div>
                <input
                    type="text"
                    required
                    value={props.username}
                    onChange={handleUsernameChange} />
            </div>
            <div>
                <label>Password</label>
            </div>
            <div>
                <input
                    type="password"
                    required
                    name="password"
                    value={props.password}
                    onChange={handlePasswordChange} />
            </div>
            <div>
                <input
                    type="submit"
                    value="Login" />
            </div>
        </form>
    </div>
}