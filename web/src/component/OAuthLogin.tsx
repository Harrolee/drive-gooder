import { FormControl, Button, Box } from "@mui/material";

export interface OAuthLoginProps {
  loginCallback: VoidFunction;
}
export default function OAuthLogin(props: OAuthLoginProps) {
  const handleOauth = () => {
    window.open(`${process.env.REACT_APP_API_ROOT}/login`, "_self");
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center">
      <FormControl>
        <Button onClick={handleOauth}>OAuth2 Login</Button>
      </FormControl>
    </Box>
  );
}
