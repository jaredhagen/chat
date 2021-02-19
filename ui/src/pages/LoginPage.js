import { Link, Redirect } from "react-router-dom";

import { SimpleForm } from "../components";
import { useLogInUser } from "../hooks";
import { SimplePage } from "../pages";

function LoginPage() {
  const logInUser = useLogInUser();

  const onFinish = (credentials) => {
    logInUser.mutate(credentials);
  };

  return logInUser.isSuccess ? (
    <Redirect push={true} to={{ pathname: "/" }}></Redirect>
  ) : (
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
