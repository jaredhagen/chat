import { Link, useHistory } from "react-router-dom";

import { SimpleForm } from "../components";
import { useRegisterUser } from "../hooks";
import SimplePage from "./SimplePage";

function LoginPage() {
  const history = useHistory();
  const registerUser = useRegisterUser();

  const onFinish = (username) => {
    registerUser.mutate(username, {
      onSuccess: () => {
        history.push("/");
      },
    });
  };

  return (
    <SimplePage
      title="Sign up to Chat"
      alternateLink={
        <Link to="/login">Been here before? Click here to log in.</Link>
      }
    >
      <SimpleForm
        buttonText="Sign up"
        errorMessage="Username already taken"
        hasError={registerUser.isError}
        isLoading={registerUser.isLoading}
        name="registerUser"
        onFinish={onFinish}
        inputName="username"
        inputPlaceholder="Username"
        inputValidationMessage="Please input a username"
      />
    </SimplePage>
  );
}

export default LoginPage;
