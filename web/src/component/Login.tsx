import { useCallback } from "react";
import { authenticate } from "../api";
import { FormControl, Button, FormLabel, TextField } from "@mui/material";

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

    return <FormControl>
        <FormLabel>Username</FormLabel>
        <TextField value={props.username} onChange={handleUsernameChange} />
        <FormLabel>Password</FormLabel>
        <TextField type="password" value={props.password} onChange={handlePasswordChange} />
        <Button onClick={handleLogin}>Login</Button>
    </FormControl>;
}