classdef Calculator
    % CALCULATOR A simple calculator class
    %
    % This class demonstrates basic arithmetic operations.

    properties
        pi (1,1) double = pi; % Value of pi
    end

    properties (Access = private)
        version (1,1) double = 1.0; % Version of the calculator
    end

    methods
        function result = add(obj, a, b)
            % ADD Add two numbers
            %
            % Args:
            %     obj (Calculator): Instance of Calculator
            %     a (double): First number
            %     b (double): Second number
            %
            % Returns:
            %     double: Sum of a and b

            result = a + b;
        end

        function result = multiply(~, a, b)
            % MULTIPLY Multiply two numbers
            %
            % Args:
            %     obj (Calculator): Instance of Calculator
            %     a (double): First number
            %     b (double): Second number
            %
            % Returns:
            %     double: Product of a and

            result = a * b;
        end
    end
end
