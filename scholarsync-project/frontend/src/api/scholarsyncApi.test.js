import { getApiError } from "./scholarsyncApi";

describe("getApiError", () => {
  test("returns server error message when present", () => {
    const error = {
      response: {
        data: {
          error: "Invalid email or password",
        },
      },
    };

    expect(getApiError(error, "Fallback")).toBe("Invalid email or password");
  });

  test("returns first field validation error when message array is present", () => {
    const error = {
      response: {
        data: {
          email: ["Email already exists"],
        },
      },
    };

    expect(getApiError(error, "Fallback")).toBe("Email already exists");
  });

  test("returns fallback when no known error shape is present", () => {
    expect(getApiError({}, "Fallback")).toBe("Fallback");
  });
});
