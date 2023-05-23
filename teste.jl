function soma(x::Int, y::Int)::Int
    if x > 0
        x = 0
    end
    ret::Int = 1
    ret = x + y
    return ret
end
b::Int = 100
a::Int = 2
a = soma(1, 2)
println(a)




