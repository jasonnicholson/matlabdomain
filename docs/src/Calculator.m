classdef Calculator
    % CALCULATOR A simple calculator class
    %
    % This class demonstrates basic arithmetic operations.

    methods
        function result = add(obj, a, b)
            % ADD Add two numbers
            %
            % Args:
            %     a (double): First number
            %     b (double): Second number
            %
            % Returns:
            %     double: Sum of a and b

            result = a + b;
        end

        function result = multiply(obj, a, b)
            % MULTIPLY Multiply two numbers
            %
            % Args:
            %     a (double): First number
            %     b (double): Second number
            %
            % Returns:
            %     double: Product of a and b

            result = a * b;
        end
    end
end
