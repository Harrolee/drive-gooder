import { FormControl, Button, Box } from "@mui/material";

export interface OAuthLoginProps {
  loginCallback: VoidFunction;
}
const API_ROOT = "https://drive-gooder.com/api";
export default function OAuthLogin(props: OAuthLoginProps) {
  const handleOauth = () => {
    window.open(`${API_ROOT}/login`, "_self");
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center">
      <FormControl>
        <h1>testing</h1>
        <Button onClick={handleOauth}>OAuth2 Login</Button>
      </FormControl>
    </Box>
  );
}
