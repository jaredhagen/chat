import { Link, useHistory } from "react-router-dom";

import { SimpleForm } from "../components";
import { useLogInUser } from "../hooks";
import SimplePage from "./SimplePage";

function LoginPage() {
  const history = useHistory();
  const logInUser = useLogInUser();

  const onFinish = (credentials) => {
    logInUser.mutate(credentials, {
      onSuccess: () => {
        history.push("/");
      },
    });
  };

  return (
    <SimplePage
      title="Log in to Chat"
      alternateLink={<Link to="/signup">New Here? Click here to sign up.</Link>}
    >
      <SimpleForm
        buttonText="Log in"
        errorMessage="Unrecognized username"
        hasError={logInUser.isError}
        isLoading={logInUser.isLoading}
        name="login"
        onFinish={onFinish}
        inputName="username"
        inputPlaceholder="Username"
        inputValidationMessage="Please input your username"
      />
    </SimplePage>
  );
}

export default LoginPage;
