function soma(x::String, y::String)::String
    ret::String = "1"
    ret = x . y
    return ret
end

b::String = "100"
a::String = "2"
b = soma("1", "2")
println(b)
