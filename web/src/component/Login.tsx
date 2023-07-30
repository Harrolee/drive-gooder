import { useCallback } from "react";

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
    const handleLogin = useCallback(() => {
        props.loginCallback();
    }, [props]);

    return <div>
        <label>Username</label>
        <input type="text" required name="username" value={props.username} onChange={handleUsernameChange} />
        <label>Password</label>
        <input type="password" required name="password" value={props.password} onChange={handlePasswordChange}/>
        <button onClick={handleLogin}>Login</button>
    </div>
}